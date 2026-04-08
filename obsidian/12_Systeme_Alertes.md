# 🔔 Système d'Alertes — JeryMotro Platform
#JeryMotro #MemoireL3 #Alerte #API #Python
[[Glossaire_Tags]] | [[00_INDEX]] | [[11_Automatisation_n8n]]

---

## 1. STRATÉGIE OFFICIELLE D'ALERTE VISUELLE (V3)

Pour maximiser l'impact sans saturer la bande passante, chaque alerte générée contiendra un maximum de **2 images explicites**. Ces images permettent de contourner la couverture nuageuse (via le thermique) et de donner un contexte clair.

| Image | Source | Rôle Principal |
|-------|--------|----------------|
| **1. Thermique (Infrarouge)** | Landsat 8/9 B10/B11 ou VIIRS | 🔴 **Priorité absolue**. Traverse partiellement les nuages, montre la chaleur. |
| **2. Visible (RGB)** | Sentinel-2 ou Landsat 8/9 | 🟢 Contexte environnemental (forêt, village, savane). |

### Matrice de Déclenchement

| Condition | Niveau | Contenu (Images) | Actions (Canaux) |
|-----------|--------|------------------|------------------|
| `risk_score > 0.80` ou `FRP > 50` | 🔴 **ALERTE HAUTE** | Thermique + Visible + (Option: Burned Area) | **Email + SMS + WhatsApp** immédiats |
| `risk_score > 0.60` | 🟠 **ALERTE MOYENNE**| Thermique + Visible | **Email + SMS + WhatsApp** (Regroupés possiblement) |
| `risk_score > 0.40` | 🟡 **ALERTE BASSE** | Seulement Thermique | **Email uniquement** |

---

## 2. AUTOMATISATION DES IMAGES (ImgBB)

Pour envoyer des images par SMS/WhatsApp sans dépasser les limites API ou sans nécessiter un stockage lourd, JeryMotro utilise une solution "Lean" et furtive via **ImgBB** :

```mermaid
graph LR
    A[Cluster Détecté] --> B[n8n déclenche Script Python]
    B --> C[Téléchargement scènes Landsat/Sentinel]
    C --> D[Génération de 2 PNG (Thermique/Visible)]
    D --> E[Upload automatique vers ImgBB]
    E --> F[Récupération des URLs directes]
    F --> G[Envoi Email / Macrodroid (SMS/WhatsApp)]
```
*Temps estimé par alerte : 30 à 90 secondes.*

## 3. IMPLÉMENTATION PYTHON (Alert Service)

```python
# api/services/alert_service.py
import requests, os
from services.twilio_sandbox import send_whatsapp
from services.macrodroid_sms import trigger_macrodroid_sms
from services.email_smtp import send_html_email

def upload_to_imgbb(image_path: str) -> str:
    """Upload un PNG généré en local vers ImgBB et retourne le lien direct."""
    url = "https://api.imgbb.com/1/upload"
    payload = {
        "key": os.getenv("IMGBB_API_KEY")
    }
    with open(image_path, "rb") as file:
        res = requests.post(url, payload, files={"image": file})
    return res.json()["data"]["url"]

def route_alert(risk_score: float, frp: float, cluster_info: dict):
    """Logique de routage de l'alerte selon la Matrice Officielle."""
    
    img_urls = []
    
    # Étape 1 : Si on déclenche, on génère au moins l'image thermique
    if risk_score > 0.40:
        thermal_path = generate_thermal_png(cluster_info['bbox'])
        img_urls.append(upload_to_imgbb(thermal_path))
        
    # Étape 2 : Si Alerte Moyenne/Haute, on ajoute le visible
    if risk_score > 0.60 or frp > 50:
        visible_path = generate_visible_png(cluster_info['bbox'])
        img_urls.append(upload_to_imgbb(visible_path))

    # Étape 3 : Structuration du message
    msg = f"🔥 Alerte JeryMotro\nRégion: {cluster_info['region']}\nRisque: {risk_score:.0%}\nImages: {' | '.join(img_urls)}"
    
    # Étape 4 : Routage
    if risk_score > 0.80 or frp > 50: # HAUTE
        send_html_email("🚨 ALERTE CRITIQUE", msg, img_urls)
        trigger_macrodroid_sms(msg)
        send_whatsapp(msg)
    elif risk_score > 0.60:           # MOYENNE
        send_html_email("🟠 Alerte Moyenne", msg, img_urls)
        trigger_macrodroid_sms(msg)
        send_whatsapp(msg)
    else:                            # BASSE
        send_html_email("🟡 Détection Mineure", msg, img_urls) # Email uniquement
```

---

## 4. TEMPLATE MESSAGE WHATSAPP / SMS (MacroDroid)

> [!tip] Astuce Macrodroid
> Au lieu de payer une API SMS pro, le backend envoie une requête HTTP (via Pushbullet ou un webhook direct) à un vieux smartphone Android. Ce téléphone utilise l'application **MacroDroid** pour capter la requête et envoyer le texto via la carte SIM personnelle (Telma/Airtel/Orange).

```
🚨 *ALERTE HAUTE JERYMOTRO*
📍 Région : {region}
⚠️ Risque : {score}% | FRP : {frp} MW

📸 *Images Satellite (Temps Réel)*
🔥 Thermique : {img_thermique_url}
🌳 Visible : {img_visible_url}

👉 Dashboard : https://jerymotro.vercel.app
```

---

*n8n → [[11_Automatisation_n8n]]*
*FastAPI → [[09_FastAPI_Backend]]*
