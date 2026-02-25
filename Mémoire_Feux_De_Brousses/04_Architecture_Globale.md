# 🏗️ Architecture Globale — FireProject
#FireProject #ThinkTank #Workflow #Python #ML #DL #n8n
[[Glossaire_Tags]] | [[00_INDEX]]

---

## 1. SCHÉMA COMPLET DE LA PLATEFORME

```
╔══════════════════════════════════════════════════════════════╗
║                    COUCHE 1 : SOURCES DE DONNÉES             ║
╠══════════════════════════════════════════════════════════════╣
║  NASA FIRMS API          ESA Copernicus        Hansen GFC    ║
║  ├── MODIS NRT           ├── Sentinel-2 L2A    └── Tree loss ║
║  ├── VIIRS SNPP NRT      └── Sentinel-1 (SAR)               ║
║  └── VIIRS NOAA-20 NRT                                       ║
╚══════════════════╦═══════════════════════════════════════════╝
                   ║  HTTP / API REST
╔══════════════════╩═══════════════════════════════════════════╗
║                COUCHE 2 : COLLECTE AUTOMATISÉE (n8n)         ║
╠══════════════════════════════════════════════════════════════╣
║  Trigger CRON → Appel APIs → Téléchargement CSV/GeoTIFF      ║
║  → Validation format → Stockage brut /data/raw/              ║
╚══════════════════╦═══════════════════════════════════════════╝
                   ║
╔══════════════════╩═══════════════════════════════════════════╗
║              COUCHE 3 : PRÉTRAITEMENT SIG (Python)           ║
╠══════════════════════════════════════════════════════════════╣
║  scripts/preprocessing/                                      ║
║  ├── filter_bbox.py      → Filtrage Madagascar               ║
║  ├── clean_firms.py      → Nettoyage doublons/NaN            ║
║  ├── compute_indices.py  → NDVI, NBR, dNBR                   ║
║  ├── temporal_align.py   → Fusion multi-capteurs             ║
║  └── patch_generator.py  → Patches 64×64 pour DL            ║
║                                                              ║
║  Sortie → /data/processed/ (CSV propre + GeoTIFF normalisé)  ║
╚══════════════════╦═══════════════════════════════════════════╝
                   ║
╔══════════════════╩═══════════════════════════════════════════╗
║           COUCHE 4 : INTELLIGENCE ML/DL (Python)             ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  ML (données tabulaires FIRMS)                               ║
║  ├── models/rf_classifier.py     → Random Forest            ║
║  ├── models/xgb_risk.py          → XGBoost prédictif         ║
║  └── models/svm_baseline.py      → SVM (comparaison)         ║
║                                                              ║
║  DL (images Sentinel-2)                                      ║
║  ├── models/cnn_classifier.py    → CNN 4 couches             ║
║  ├── models/resnet_transfer.py   → ResNet-18 transfer        ║
║  ├── models/unet_segmentation.py → U-Net segmentation        ║
║  └── models/lstm_timeseries.py   → LSTM prédictif            ║
║                                                              ║
║  Sortie → /data/predictions/ (scores + masques)              ║
╚══════════════════╦═══════════════════════════════════════════╝
                   ║
╔══════════════════╩═══════════════════════════════════════════╗
║              COUCHE 5 : STOCKAGE STRUCTURÉ                   ║
╠══════════════════════════════════════════════════════════════╣
║  /data/db/fireproject.sqlite                                 ║
║  ├── TABLE detections      → feux détectés (date, GPS, FRP)  ║
║  ├── TABLE predictions_ml  → scores risque par zone          ║
║  ├── TABLE regions_risk    → zones à risque 48–72h           ║
║  ├── TABLE deforestation   → évolution forestière            ║
║  └── TABLE alerts_log      → historique alertes envoyées     ║
╚══════════════════╦═══════════════════════════════════════════╝
                   ║
╔══════════════════╩═══════════════════════════════════════════╗
║          COUCHE 6 : ORCHESTRATION n8n                        ║
╠══════════════════════════════════════════════════════════════╣
║  Workflows :                                                 ║
║  ├── daily_collection.json   (CRON 06h → API → BDD)          ║
║  ├── ml_inference.json       (BDD → Python → scores)         ║
║  ├── alert_trigger.json      (score > 0.7 → IA générative)  ║
║  ├── weekly_report.json      (agrégation → PDF → envoi)      ║
║  └── sentinel_sync.json      (CRON 5j → S2 → prétraitement) ║
╚══════════════════╦═══════════════════════════════════════════╝
                   ║
╔══════════════════╩═══════════════════════════════════════════╗
║          COUCHE 7 : IA GÉNÉRATIVE                            ║
╠══════════════════════════════════════════════════════════════╣
║  Option 1 (recommandé) : Ollama local                        ║
║  ├── Modèle : Llama 3 8B ou Mistral 7B                       ║
║  ├── Endpoint : http://localhost:11434/api/generate           ║
║  └── Avantage : gratuit, souverain, illimité                 ║
║                                                              ║
║  Option 2 (backup) : Groq API                                ║
║  ├── Modèle : llama3-8b-8192                                 ║
║  └── Endpoint : https://api.groq.com/openai/v1/chat          ║
║                                                              ║
║  Prompt type → rapport structuré en français/malgache        ║
╚══════════════════╦═══════════════════════════════════════════╝
                   ║
╔══════════════════╩═══════════════════════════════════════════╗
║          COUCHE 8 : SORTIES DÉCISIONNELLES                   ║
╠══════════════════════════════════════════════════════════════╣
║  ├── dashboard/map.html    → Carte Folium interactive        ║
║  ├── reports/daily_XX.pdf  → Rapport quotidien IA            ║
║  ├── alerts/email_XX.html  → Email d'alerte structuré        ║
║  └── api/v1/              → API REST pour partenaires        ║
╚══════════════════════════════════════════════════════════════╝
```

---

## 2. STRUCTURE DES DOSSIERS DU PROJET

```
fireproject/
│
├── 📁 data/
│   ├── raw/                    # Données brutes téléchargées
│   │   ├── firms/              # CSV FIRMS MODIS + VIIRS
│   │   ├── sentinel2/          # GeoTIFF Sentinel-2
│   │   └── hansen/             # Données déforestation
│   ├── processed/              # Données après prétraitement
│   │   ├── firms_clean.csv
│   │   ├── patches/            # Patches 64×64 pour DL
│   │   └── indices/            # NDVI, NBR calculés
│   ├── predictions/            # Sorties ML/DL
│   └── db/
│       └── fireproject.sqlite  # Base de données principale
│
├── 📁 scripts/
│   ├── preprocessing/
│   │   ├── filter_bbox.py
│   │   ├── clean_firms.py
│   │   ├── compute_indices.py
│   │   └── patch_generator.py
│   ├── models/
│   │   ├── rf_classifier.py
│   │   ├── xgb_risk.py
│   │   ├── cnn_classifier.py
│   │   ├── unet_segmentation.py
│   │   └── lstm_timeseries.py
│   ├── inference/
│   │   ├── run_ml.py           # Inférence ML sur nouvelles données
│   │   └── run_dl.py           # Inférence DL sur images
│   └── utils/
│       ├── db_utils.py         # Fonctions BDD SQLite
│       ├── api_utils.py        # Fonctions appel APIs
│       └── plot_utils.py       # Visualisation / cartes
│
├── 📁 n8n/
│   ├── daily_collection.json
│   ├── ml_inference.json
│   ├── alert_trigger.json
│   ├── weekly_report.json
│   └── sentinel_sync.json
│
├── 📁 notebooks/               # Jupyter notebooks (exploration)
│   ├── 01_EDA_FIRMS.ipynb
│   ├── 02_Preprocessing.ipynb
│   ├── 03_ML_Baseline.ipynb
│   ├── 04_CNN_Training.ipynb
│   ├── 05_UNet_Training.ipynb
│   └── 06_LSTM_Training.ipynb
│
├── 📁 dashboard/
│   ├── map.html                # Carte Folium interactive
│   └── assets/
│
├── 📁 reports/                 # Rapports générés automatiquement
│
├── 📁 models_saved/            # Modèles entraînés sauvegardés
│   ├── rf_model.pkl
│   ├── xgb_model.pkl
│   ├── cnn_model.h5
│   ├── unet_model.h5
│   └── lstm_model.h5
│
├── requirements.txt
├── README.md
└── config.yaml                 # Configuration (API keys, bbox, seuils)
```

---

## 3. FLUX DE DONNÉES DÉTAILLÉ

### 3.1 Données FIRMS (quotidien)

```
API FIRMS
└── GET /api/area/csv/[MAP_KEY]/VIIRS_SNPP_NRT/43.0,-25.6,50.5,-11.9/1
    └── CSV brut (colonnes : latitude, longitude, brightness,
                  scan, track, acq_date, acq_time, satellite,
                  confidence, version, bright_t31, frp, daynight)
        └── filter_bbox.py → Madagascar uniquement
            └── clean_firms.py → nettoyage + features
                └── rf_classifier.py → score feu (0–1)
                    └── BDD → TABLE detections + predictions_ml
                        └── n8n : si score > 0.7 → alerte
```

### 3.2 Données Sentinel-2 (tous les 5 jours)

```
API Sentinel Hub
└── GET images bandes B04, B08, B11, B12 (SWIR)
    └── compute_indices.py → NDVI, NBR, dNBR
        └── patch_generator.py → patches 64×64
            └── unet_segmentation.py → masque zones brûlées
                └── BDD → TABLE deforestation
```

---

## 4. CONFIGURATION (config.yaml)

```yaml
# Configuration FireProject
project:
  name: "FireProject Madagascar"
  version: "1.0.0"

bbox_madagascar:
  west: 43.0
  south: -25.6
  east: 50.5
  north: -11.9

apis:
  firms_map_key: "VOTRE_MAP_KEY_ICI"
  nasa_earthdata_token: "VOTRE_TOKEN_ICI"
  groq_api_key: "gsk_..."  # Optionnel backup

ml:
  alert_threshold: 0.70       # Score minimum pour déclencher alerte
  confidence_min: 30          # Confiance FIRMS minimum (%)
  frp_significant: 10.0       # FRP minimum pour feu significatif (MW)
  train_test_split: [0.70, 0.15, 0.15]

dl:
  patch_size: 64              # Taille patches images (pixels)
  batch_size: 32
  epochs: 50
  learning_rate: 0.001

n8n:
  daily_cron: "0 6 * * *"    # 06h00 chaque jour
  weekly_cron: "0 8 * * 1"   # Lundi 08h00
  sentinel_cron: "0 7 */5 * *" # Tous les 5 jours 07h00

ollama:
  endpoint: "http://localhost:11434/api/generate"
  model: "llama3"
  max_tokens: 1000
```

---

## 5. MÉTRIQUES DE SUCCÈS PAR MODÈLE

| Modèle | Métrique principale | Seuil minimum | Seuil cible |
|--------|--------------------| --------------|-------------|
| Random Forest | F1-Score (classe feu) | 0.78 | 0.85 |
| XGBoost | AUC-ROC | 0.82 | 0.90 |
| CNN classification | Accuracy | 0.80 | 0.88 |
| U-Net segmentation | IoU | 0.65 | 0.75 |
| LSTM prédictif | MAE (jours) | < 1.5j | < 1j |

---

*Pipeline ML/DL → [[06_Pipeline_ML_DL]]*
*Automatisation → [[07_Automatisation_n8n]]*
*APIs → [[05_APIs_et_Donnees]]*
