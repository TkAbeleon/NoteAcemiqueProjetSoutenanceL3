# 🏗️ Architecture Globale — JeryMotro Platform v2.2
#JeryMotro #MemoireL3 #Workflow #Docker #FastAPI #Python
[[Glossaire_Tags]] | [[00_INDEX]] | [[01_Cahier_des_Charges]]

---

## 1. PIPELINE COMPLET

```
┌─────────────────────────────────────────────────────────────┐
│  SOURCE : NASA FIRMS API (toutes les 30 min via n8n)        │
│  ├── MODIS_NRT                                              │
│  ├── VIIRS_SNPP_NRT          Bbox : -25.5,43,-11.5,50       │
│  └── VIIRS_NOAA21_NRT                                       │
└────────────────────┬────────────────────────────────────────┘
                     ↓ CSV brut
┌────────────────────────────────────────────────────────────┐
│  PYTHON PREPROCESSING (scripts/preprocessing/)             │
│  ├── fetch_firms.py     → appel API + sauvegarde CSV       │
│  ├── clean_firms.py     → nettoyage + validation           │
│  └── feature_engineering.py                               │
│       ├── diff_brightness = brightness - bright_t31        │
│       ├── frp_log = log1p(frp)                             │
│       ├── local_hour = UTC + 3                             │
│       ├── is_dry_season = mois ∈ [4,5,6,7,8,9,10]         │
│       └── ERA5 via GEE (temp, humidité, vent)              │
└────────────────────┬───────────────────────────────────────┘
                     ↓ DataFrame enrichi
┌────────────────────────────────────────────────────────────┐
│  HDBSCAN CLUSTERING (scripts/clustering/)                  │
│  ├── Rayon spatial : 750m                                  │
│  ├── Fenêtre temporelle : 48h                              │
│  └── min_cluster_size : 3 points                           │
│  Sortie : cluster_id, cluster_size, cluster_frp_total      │
└────────────────────┬───────────────────────────────────────┘
                     ↓ Features + clusters
┌────────────────────────────────────────────────────────────┐
│  MADFIRENET — MODÈLE ORIGINAL (scripts/models/)            │
│  ├── Branche A : XGBoost                                   │
│  │   ├── Entrée : features FIRMS + ERA5 + cluster_features │
│  │   └── Sortie : fire_risk (0/1) + risk_score (0.0–1.0)  │
│  └── Branche B : ConvLSTM                                  │
│      ├── Entrée : séries temporelles 7j sur grille 375m    │
│      └── Sortie : carte risque J+1 (grille Madagascar)     │
└────────────────────┬───────────────────────────────────────┘
                     ↓ Résultats JSON
┌────────────────────────────────────────────────────────────┐
│  STOCKAGE                                                  │
│  ├── PostgreSQL : détections + prédictions + clusters      │
│  └── ChromaDB   : embeddings résultats (RAG pour IA)       │
└────────────────────┬───────────────────────────────────────┘
                     ↓ ORM SQLAlchemy
┌────────────────────────────────────────────────────────────┐
│  FASTAPI BACKEND (api/)                                    │
│  ├── GET /detections        → points feux filtrés          │
│  ├── GET /predictions       → sorties JeryMotroNet           │
│  ├── GET /clusters          → résultats HDBSCAN            │
│  ├── GET /risk-map          → grille ConvLSTM J+1          │
│  ├── GET /alerts            → historique alertes           │
│  ├── POST /chat             → proxy Groq + RAG ChromaDB    │
│  └── GET /docs              → Swagger UI auto              │
└──────────┬─────────────────────────┬───────────────────────┘
           ↓ JSON REST               ↓ IF score > 0.7 / FRP > 50MW
┌──────────────────┐      ┌──────────────────────────────────┐
│  FRONTEND        │      │  SYSTÈME D'ALERTES               │
│  (React ou       │      │  ├── Email (smtplib)             │
│   Flutter Web)   │      │  └── WhatsApp (Twilio Sandbox)   │
│  ├── Carte       │      └──────────────────────────────────┘
│  ├── Dashboard   │
│  ├── Chat IA     │
│  └── Alertes     │
└──────────────────┘
```

---

## 2. INFRASTRUCTURE DOCKER

Voir détail → [[08_Docker_Infrastructure]]

```
docker-compose.yml
├── madfire-api       (FastAPI — port 8000)
├── madfire-frontend  (React/Flutter Web — port 3000)
├── madfire-n8n       (Automatisation — port 5678)
├── madfire-chromadb  (RAG — port 8001)
└── madfire-db        (PostgreSQL — port 5432)
```

**Réseau Docker interne :** `madfire-network`
Tous les services communiquent par nom de service (ex: `http://madfire-api:8000`).

---

## 3. STRUCTURE DES DOSSIERS

```
madfire-platform/
│
├── 📁 api/                        # FastAPI Backend
│   ├── main.py                    # App FastAPI + routers
│   ├── routers/
│   │   ├── detections.py
│   │   ├── predictions.py
│   │   ├── clusters.py
│   │   ├── alerts.py
│   │   └── chat.py
│   ├── models/
│   │   ├── detection.py           # SQLAlchemy ORM
│   │   ├── prediction.py
│   │   └── alert.py
│   ├── schemas/
│   │   ├── detection.py           # Pydantic schemas
│   │   └── prediction.py
│   ├── services/
│   │   ├── madflrenet_service.py  # Inférence ML/DL
│   │   ├── rag_service.py         # Groq + ChromaDB
│   │   └── alert_service.py      # Email + Twilio
│   ├── database.py                # SQLAlchemy setup
│   ├── requirements.txt
│   └── Dockerfile
│
├── 📁 frontend/                   # React ou Flutter
│   ├── (React) src/
│   │   ├── components/
│   │   │   ├── MapView.jsx        # Carte Leaflet
│   │   │   ├── Dashboard.jsx      # Graphiques
│   │   │   ├── ChatPanel.jsx      # JeryMotro AI
│   │   │   └── AlertPanel.jsx
│   │   ├── services/
│   │   │   └── api.js             # Appels FastAPI
│   │   └── App.jsx
│   ├── package.json
│   └── Dockerfile
│
├── 📁 ml/                         # Scripts ML/DL
│   ├── preprocessing/
│   │   ├── fetch_firms.py
│   │   ├── clean_firms.py
│   │   └── feature_engineering.py
│   ├── clustering/
│   │   └── hdbscan_cluster.py
│   ├── models/
│   │   ├── xgboost_classifier.py
│   │   ├── convlstm_predictor.py
│   │   └── rf_regression.py      # Should Have
│   ├── inference/
│   │   └── run_madfirenet.py
│   └── notebooks/
│       ├── 01_EDA_FIRMS.ipynb
│       ├── 02_Feature_Engineering.ipynb
│       ├── 03_XGBoost_Training.ipynb
│       └── 04_ConvLSTM_Training.ipynb
│
├── 📁 n8n/
│   └── workflows/
│       ├── daily_collection.json
│       ├── alert_trigger.json
│       └── weekly_report.json
│
├── 📁 data/
│   ├── raw/firms/                 # CSV bruts MODIS + VIIRS
│   ├── processed/                 # Données nettoyées + features
│   └── models_saved/              # .pkl + .pth modèles
│
├── docker-compose.yml
├── .env.example                   # Clés API (jamais committer .env)
├── .gitignore
└── README.md
```

---

## 4. FLUX DE DONNÉES DÉTAILLÉ

### 4.1 Collecte → Stockage (toutes les 30 min)

```python
# Flux n8n → Python → PostgreSQL
1. n8n CRON déclenche GET /api/area/csv/{KEY}/VIIRS_SNPP_NRT/-25.5,43,-11.5,50/1
2. fetch_firms.py reçoit CSV brut
3. clean_firms.py : filtre confidence >= 'nominal', frp >= 1.0
4. feature_engineering.py : calcule diff_brightness, frp_log, etc.
5. hdbscan_cluster.py : groupe les points en clusters
6. run_madfirenet.py : inférence XGBoost + ConvLSTM
7. INSERT INTO detections, predictions, clusters (PostgreSQL)
8. ChromaDB.add() : embed résultats pour RAG
9. IF score > 0.7 OU frp > 50 → alert_service.py
```

### 4.2 Frontend → FastAPI → BDD

```
Utilisateur → React/Flutter
    → GET /api/detections?date=today&min_risk=0.5
    → FastAPI route → SQLAlchemy query → PostgreSQL
    → Retour JSON → Leaflet affiche les points
```

### 4.3 Chat JeryMotro AI

```
Utilisateur → "Quelle zone est la plus touchée cette semaine ?"
    → POST /api/chat {message: "..."}
    → RAG Service : query ChromaDB → top 5 contextes pertinents
    → Groq API : prompt = contexte + question
    → Réponse limitée aux données du projet (pas de généralités)
    → Retour JSON → Frontend affiche la réponse
```

---

## 5. MÉTRIQUES DE SUCCÈS

| Composant | Métrique | Seuil |
|-----------|----------|-------|
| JeryMotroNet XGBoost | Recall petits feux vs NASA brut | +25% |
| JeryMotroNet ConvLSTM | MAE prédiction J+1 (km²) | < 200 km² |
| FastAPI | Latence moyenne endpoint | < 200ms |
| Pipeline complet | Latence collecte → prédiction | < 5 min |
| Alertes | Latence après publication FIRMS | < 30 min |
| HDBSCAN | Cohérence clusters (silhouette) | > 0.50 |

---

*Cahier des charges → [[01_Cahier_des_Charges]]*
*Docker → [[08_Docker_Infrastructure]]*
*FastAPI → [[09_FastAPI_Backend]]*
*Frontend → [[10_Frontend_Decision]]*
*JeryMotroNet → [[04_JeryMotroNet]]*
