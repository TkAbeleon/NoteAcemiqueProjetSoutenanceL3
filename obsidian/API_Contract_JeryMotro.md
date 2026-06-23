# 📖 Contrat d'API — JeryMotro Platform (V2.2.0)

Ce document consolide le contrat d'API complet pour le backend FastAPI de la plateforme JeryMotro, généré à partir de l'analyse documentaire du projet.

## 📌 Informations Générales
- **Base URL** : `http://localhost:8000/api`
- **Format de données** : JSON (`application/json`)
- **Version API** : 2.2.0
- **Documentation Interactive** : `http://localhost:8000/docs` (Swagger UI)

---

## 🟢 Santé du Service (Health)

### `GET /health` ou `GET /`
Vérification de la disponibilité du backend.

- **Requête** : Aucun paramètre.
- **Réponse (200 OK)** :
  ```json
  {
    "status": "healthy",
    "version": "2.2.0"
  }
  ```

---

## 🔥 Détections (FIRMS)

### `GET /detections/`
Récupère les détections de feux avec leurs scores JeryMotroNet.

- **Paramètres de requête (Query)** :
  - `date_from` (date, optionnel) : Date de début.
  - `date_to` (date, optionnel) : Date de fin.
  - `min_frp` (float, optionnel) : FRP minimum en MW. Défaut: 0.0.
  - `min_risk` (float, optionnel) : Score de risque minimum (0-1).
  - `source` (string, optionnel) : MODIS, VIIRS_SNPP, VIIRS_NOAA21.
  - `limit` (int, optionnel) : Nombre max de résultats. Défaut: 50 (ou 1000 selon endpoint).
- **Réponse (200 OK)** :
  ```json
  {
    "detections": [
      {
        "id": 1,
        "latitude": -18.234,
        "longitude": 44.567,
        "frp": 87.3,
        "confidence": "high",
        "acq_date": "2026-02-23",
        "acq_time": "0845",
        "source": "VIIRS_NOAA21",
        "risk_score": 0.84,
        "niveau_risque": "CRITIQUE"
      }
    ],
    "count": 1
  }
  ```

### `POST /detections/` (Interne / n8n)
Soumet des données brutes FIRMS pour enrichissement (GEE), prédiction ML, et stockage.

- **Corps de la requête (JSON)** : Données brutes de détection.
- **Réponse (201 Created)** : Succès de l'enregistrement. Déclenche une alerte en arrière-plan si `risk_score > 0.70` ou `FRP > 50`.

---

## 🗺️ Clusters (Hotspots)

### `GET /clusters/`
Récupère les zones de concentration de feux.

- **Paramètres de requête (Query)** :
  - `limit` (int, optionnel) : Nombre de clusters (Défaut: 20).
- **Réponse (200 OK)** :
  ```json
  [
    {
      "id": 402,
      "center_lat": -21.45,
      "center_lon": 47.11,
      "frp_max": 85.3,
      "frp_total": 210.5,
      "cluster_size": 5,
      "date": "2026-03-30T09:40:00Z"
    }
  ]
  ```

---

## 🔮 Prédictions & Risques (MadFireNet)

### `GET /predictions/`
Retourne les prédictions de risque d'incendie pour J+1 par région.

- **Paramètres de requête (Query)** :
  - `date` (date, optionnel)
  - `region` (string, optionnel) : ex. "Menabe", "Boeny".

### `POST /predictions/`
Évaluation à la volée du risque via le modèle XGBoost basé sur des métriques transmises.

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
- **Réponse (200 OK)** :
  ```json
  {
    "risk_score": 0.89,
    "niveau_risque": "CRITIQUE",
    "model_version": "XGBoost-V2-Prototype"
  }
  ```

### `GET /risk-map`
Retourne la grille spatiale de risque (ConvLSTM).

- **Paramètres de requête (Query)** :
  - `date` (date, requis)
  - `format` (string, optionnel) : `geojson` ou `json` (Défaut: `geojson`).
- **Réponse (200 OK)** : Objet GeoJSON prêt à être affiché (ex: Leaflet).

---

## 🔔 Système d'Alertes

### `GET /alerts/`
Historique des alertes déclenchées.

- **Paramètres de requête (Query)** :
  - `limit` (int, optionnel) : Défaut: 20.
- **Réponse (200 OK)** :
  ```json
  [
    {
      "id": 1,
      "detection_id": 16755,
      "message": "🔥 ALERTE: Feu Critique détecté dans le Menabe.",
      "status": "sent",
      "sent_at": "2026-05-02T10:00:00Z"
    }
  ]
  ```

### `POST /alerts/subscribe`
Inscription aux notifications d'urgence.

- **Corps de la requête (JSON)** :
  ```json
  {
    "email": "ranger@madagascar.mg",
    "phone_number": "+261340000000",
    "region_preference": "Menabe"
  }
  ```
- **Réponse (200 OK)** : Confirmation de l'enregistrement.

---

## 🧠 Intelligence Artificielle (JeryMotro AI)

### `POST /chat/`
Chatbot RAG basé sur ChromaDB et Groq (Llama-3).

- **Corps de la requête (JSON)** :
  ```json
  {
    "message": "Quelles sont les détections d'aujourd'hui dans le Menabe ?"
  }
  ```
- **Réponse (200 OK)** :
  ```json
  {
    "response": "Aujourd'hui, 52 foyers d'incendie ont été détectés, avec une activité concentrée dans la région du Menabe (FRP max de 187 MW).",
    "sources": ["ChromaDB: Résumé Journalier"],
    "data_context": {}
  }
  ```
