# 📖 Documentation API — JeryMotro Platform (V2)
#JeryMotro #API #Documentation #FastAPI
[[Glossaire_Tags]] | [[00_INDEX]] | [[09_FastAPI_Backend]]

> Ce document référence l'ensemble des points d'entrée (endpoints) disponibles sur le backend FastAPI développé pour le prototype JeryMotro. L'API tourne par défaut sur `http://localhost:8000`.

---

## 🟢 Santé du Service (Healthcheck)

### `GET /api/health`
Permet de vérifier si le backend est en ligne et accessible.

- **Paramètres** : Aucun
- **Réponse attendue (200 OK)** :
```json
{
  "status": "ok",
  "system": "JeryMotro Platform Backend"
}
```

---

## 🔥 Données Géospatiales

### `GET /api/detections/`
Récupère les détections de feux brutes issues de FIRMS (NASA).

- **Paramètres (Query)** :
  - `limit` *(int, optionnel)* : Nombre maximum de résultats (défaut: 50).
  - `min_frp` *(float, optionnel)* : Filtre pour exclure les feux ayant une puissance radiative inférieure (défaut: 0.0).
- **Réponse attendue (200 OK)** :
```json
[
  {
    "id": 16755,
    "source": "MODIS_NRT",
    "latitude": -18.765,
    "longitude": 46.123,
    "acq_datetime": "2026-03-30T10:15:00Z",
    "frp": 12.5,
    "confidence": "high"
  }
]
```

### `GET /api/clusters/`
Récupère les zones concentrées de feux (hotspots) identifiées pour réduire le bruit visuel sur la carte.

- **Paramètres (Query)** :
  - `limit` *(int, optionnel)* : Nombre de clusters à retourner (défaut: 20).
- **Réponse attendue (200 OK)** :
```json
[
  {
    "id": 402,
    "source": "VIIRS_NOAA20_NRT",
    "latitude": -21.45,
    "longitude": 47.11,
    "acq_datetime": "2026-03-30T09:40:00Z",
    "frp": 85.3
  }
]
```

---

## 🔔 Système d'Alertes

### `GET /api/alerts/`
Récupère l'historique des alertes déclenchées par le système JeryMotro.

- **Paramètres (Query)** :
  - `limit` *(int, optionnel)* : Défaut 20.
- **Réponse attendue (200 OK)** :
```json
[
  {
    "id": 1,
    "message": "🔥 ALERTE: Feu Critique détecté dans le Menabe.",
    "status": "sent",
    "sent_at": "2026-05-02T10:00:00Z",
    "created_at": "2026-05-02T10:00:00Z",
    "user": null
  }
]
```

### `POST /api/alerts/subscribe`
Inscrit un nouvel utilisateur au système de notification d'urgences (Email/SMS).

- **Corps de la requête (JSON)** :
```json
{
  "email": "ranger@madagascar.mg",
  "phone_number": "+261340000000",
  "region_preference": "Menabe"
}
```
- **Réponse attendue (200 OK)** :
```json
{
  "message": "Abonnement enregistré avec succès",
  "email": "ranger@madagascar.mg"
}
```

---

## 🧠 Intelligence Artificielle & Machine Learning

### `POST /api/predictions/`
Envoie des caractéristiques géospatiales et météorologiques au modèle XGBoost (MadFireNet) pour obtenir une évaluation du risque d'incendie.

- **Corps de la requête (JSON)** :
```json
{
  "frp": 45.6,
  "diff_brightness": 12.3,
  "local_hour": 14,
  "is_dry_season": 1,
  "cluster_size": 3,
  "temperature_2m": 31.5,
  "slope_deg": 15.2,
  "ndvi_10m": 0.45
}
```
- **Réponse attendue (200 OK)** :
```json
{
  "risk_score": 0.89,
  "niveau_risque": "CRITIQUE",
  "model_version": "XGBoost-V2-Prototype"
}
```

### `POST /api/chat/`
Interagit avec JeryMotro AI (RAG via Groq et ChromaDB) en langage naturel.

- **Corps de la requête (JSON)** :
```json
{
  "message": "Quelles sont les détections d'aujourd'hui dans le Menabe ?"
}
```
- **Réponse attendue (200 OK)** :
```json
{
  "response": "Aujourd'hui, 52 foyers d'incendie ont été détectés, avec une activité concentrée dans la région du Menabe (FRP max de 187 MW).",
  "sources": [
    "ChromaDB: Résumé Journalier"
  ]
}
```

---
*Fin de la spécification API. Interface visuelle disponible sur `http://localhost:8000/docs` via Swagger UI.*
