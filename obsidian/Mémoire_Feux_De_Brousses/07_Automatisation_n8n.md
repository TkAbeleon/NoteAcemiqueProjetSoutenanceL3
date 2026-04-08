# ⚙️ Automatisation n8n — FireProject
#FireProject #n8n #Workflow #Alerte #API #Python
[[Glossaire_Tags]] | [[00_INDEX]]

---

## 1. RÔLE DE n8n DANS LE PROJET

> n8n est le **chef d'orchestre** de toute la plateforme.
> Il relie APIs → Python → BDD → IA générative → Alertes.
> Aucune intervention manuelle nécessaire après configuration.

**Pourquoi n8n et pas cron + scripts ?**
- Interface visuelle → débogage plus facile
- Reconnexion automatique si API échoue
- Gestion des erreurs native
- Intégration HTTP, Python, SQLite, email en natif

---

## 2. INSTALLATION n8n

### Option 1 — Self-hosted (recommandé pour contrôle total)

```bash
# Via Docker (plus stable)
docker run -it --rm \
  --name n8n \
  -p 5678:5678 \
  -v ~/.n8n:/home/node/.n8n \
  n8nio/n8n

# Accès : http://localhost:5678
```

### Option 2 — n8n Cloud (gratuit 14j trial)

```
https://app.n8n.cloud
```

---

## 3. WORKFLOW 1 — daily_collection

**Déclencheur :** CRON `0 6 * * *` (tous les jours à 06h00)
**Durée estimée :** ~5–10 minutes

```
[CRON Trigger] 
    → [HTTP Request : FIRMS VIIRS SNPP]
    → [HTTP Request : FIRMS MODIS NRT]
    → [Code Python/Node : Fusion + déduplication]
    → [Write File : data/raw/firms/YYYY-MM-DD.csv]
    → [Execute Command : python scripts/preprocessing/clean_firms.py]
    → [SQLite : INSERT INTO detections]
    → [IF : count > 0]
        → [Execute Command : python scripts/inference/run_ml.py]
        → [SQLite : UPDATE predictions_ml]
        → [Trigger : alert_trigger workflow]
```

### Configuration nœud HTTP Request (FIRMS)

```json
{
  "method": "GET",
  "url": "https://firms.modaps.eosdis.nasa.gov/api/area/csv/{{MAP_KEY}}/VIIRS_SNPP_NRT/43.0,-25.6,50.5,-11.9/1",
  "responseFormat": "text",
  "timeout": 30000
}
```

---

## 4. WORKFLOW 2 — ml_inference

**Déclencheur :** Appelé par daily_collection après collecte
**Durée estimée :** ~2–5 minutes

```
[Webhook Trigger]
    → [SQLite : SELECT * FROM detections WHERE date = TODAY AND score IS NULL]
    → [Execute Command : python run_ml.py --date TODAY]
    → [Code : Parse JSON output du script Python]
    → [SQLite : UPDATE detections SET score=... WHERE id=...]
    → [IF : any score > 0.70]
        → [Set : alert_data = zones à risque filtrées]
        → [Trigger : alert_generator workflow]
```

### Script Python appelé par n8n

```python
# scripts/inference/run_ml.py
import sys, json, joblib, pandas as pd
from datetime import date

def run_inference(target_date):
    model = joblib.load("models_saved/rf_model.pkl")

    df = pd.read_csv(f"data/processed/firms_{target_date}.csv")
    X = df[FEATURE_COLS].fillna(0)
    df['risk_score'] = model.predict_proba(X)[:, 1]

    # Sortie JSON pour n8n
    high_risk = df[df['risk_score'] > 0.70][
        ['latitude', 'longitude', 'frp', 'risk_score', 'acq_date']
    ].to_dict('records')

    print(json.dumps({
        "total_detections": len(df),
        "high_risk_count": len(high_risk),
        "high_risk_zones": high_risk
    }))

if __name__ == "__main__":
    run_inference(sys.argv[1] if len(sys.argv) > 1 else str(date.today()))
```

---

## 5. WORKFLOW 3 — alert_generator

**Déclencheur :** Appelé si score > 0.70
**Durée estimée :** ~1–2 minutes

```
[Webhook Trigger : reçoit alert_data JSON]
    → [Code : Construire prompt structuré]
    → [HTTP Request : Ollama API (local)]
         OU
    → [HTTP Request : Groq API (backup)]
    → [Code : Parser réponse IA]
    → [Write File : reports/alert_YYYY-MM-DD.txt]
    → [Send Email : alertes@fireproject.mg]
    → [SQLite : INSERT INTO alerts_log]
```

### Prompt structuré pour l'IA générative

```javascript
// Code node n8n
const data = $json.alert_data;

const prompt = `
Tu es un expert en environnement à Madagascar. 
Rédige un rapport d'alerte CONCIS et CLAIR pour les décideurs.

DONNÉES DU ${data.date} :
- Détections totales FIRMS : ${data.total_detections}
- Feux à risque élevé : ${data.high_risk_count}
- Zones principales concernées : ${data.top_regions.join(', ')}
- FRP maximum observé : ${data.frp_max} MW
- Score de risque maximum : ${(data.risk_max * 100).toFixed(0)}%
- Prédiction ML : risque élevé dans ${data.predicted_hours}h

Génère un rapport avec :
1. RÉSUMÉ (2 phrases)
2. ZONES PRIORITAIRES (liste des 3 zones les plus menacées)
3. RECOMMANDATIONS (actions immédiates)
4. NIVEAU D'ALERTE : FAIBLE / MODÉRÉ / ÉLEVÉ / CRITIQUE

Langue : Français. Longueur : 200–300 mots maximum.
`;

return { prompt };
```

### Appel Ollama (nœud HTTP Request)

```json
{
  "method": "POST",
  "url": "http://localhost:11434/api/generate",
  "body": {
    "model": "llama3",
    "prompt": "{{$json.prompt}}",
    "stream": false
  }
}
```

### Appel Groq (backup)

```json
{
  "method": "POST",
  "url": "https://api.groq.com/openai/v1/chat/completions",
  "headers": {
    "Authorization": "Bearer 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"
  },
  "body": {
    "model": "llama3-8b-8192",
    "messages": [
      {"role": "user", "content": "{{$json.prompt}}"}
    ],
    "max_tokens": 500
  }
}
```

---

## 6. WORKFLOW 4 — weekly_report

**Déclencheur :** CRON `0 8 * * 1` (lundi 08h00)

```
[CRON Trigger]
    → [SQLite : SELECT agrégats semaine (count, FRP moyen, zones)]
    → [Code : Construire prompt rapport hebdomadaire]
    → [HTTP Request : Ollama / Groq]
    → [Execute Command : python generate_pdf_report.py]
    → [Send Email : rapport PDF en pièce jointe]
    → [SQLite : INSERT INTO alerts_log type='weekly']
```

---

## 7. WORKFLOW 5 — sentinel_sync

**Déclencheur :** CRON `0 7 */5 * *` (tous les 5 jours)

```
[CRON Trigger]
    → [Execute Command : python scripts/download_sentinel2.py]
    → [Execute Command : python scripts/preprocessing/compute_indices.py]
    → [Execute Command : python scripts/inference/run_unet.py]
    → [SQLite : UPDATE deforestation]
    → [IF : déforestation détectée > seuil]
        → [HTTP Request : Ollama → rapport déforestation]
```

---

## 8. GESTION DES ERREURS

### Stratégie de retry

```
Chaque nœud HTTP Request :
- Retry On Fail : OUI
- Max Tries : 3
- Wait Between Tries : 60 secondes
```

### Notifications d'erreur

```
Error Trigger (global)
    → Send Email : "ERREUR FireProject - {{$json.error}}"
    → SQLite : INSERT INTO errors_log
```

---

## 9. VARIABLES D'ENVIRONNEMENT n8n

```bash
# À configurer dans Settings > Variables

FIRMS_MAP_KEY=VOTRE_MAP_KEY
GROQ_API_KEY=gsk_...
OLLAMA_ENDPOINT=http://localhost:11434
ALERT_EMAIL=alertes@fireproject.mg
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
DB_PATH=/home/user/fireproject/data/db/fireproject.sqlite
```

---

*Architecture → [[04_Architecture_Globale]]*
*Pipeline ML → [[06_Pipeline_ML_DL]]*
