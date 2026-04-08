# ⚙️ Feature Engineering — JeryMotro Platform
#JeryMotro #MemoireL3 #ML #DataCleaning #Python
[[Glossaire_Tags]] | [[00_INDEX]] | [[04_JeryMotroNet]]

---

## Features FIRMS de Base

| Feature | Formule | Rôle ML |
|---------|---------|---------|
| `diff_brightness` | `brightness - bright_t31` | **Feature clé** : différence thermique feu réel vs fond |
| `frp_log` | `log1p(frp)` | Normaliser la distribution très asymétrique du FRP |
| `local_hour` | `acq_time_int // 100 + 3` (UTC→EAT) | Profil diurne des feux (pics 14h–17h) |
| `is_dry_season` | `month ∈ {4,5,6,7,8,9,10}` | Saison sèche Madagascar : risque x3 |
| `daynight_bin` | `D=1 / N=0` | Les feux nocturnes ont une dynamique différente |
| `confidence_num` | `high=90, nominal=65, low=30` | Confiance VIIRS → numérique |
| `scan_track_ratio` | `scan / track` | Distorsion géométrique (coin de fauchée = moins fiable) |

## Features Clusters HDBSCAN

| Feature | Description |
|---------|-------------|
| `cluster_size` | Nb points dans le cluster (feux isolés vs grands) |
| `cluster_frp_total` | Puissance rayonnée totale du cluster (MW) |
| `cluster_frp_max` | FRP maximum dans le cluster |
| `is_noise` | Point isolé HDBSCAN (cluster_id = -1) |

## Features ERA5 & Contexte (Google Earth Engine)

| Feature | Description | Rôle ML |
|---------|-------------|---------|
| `temperature_2m` | Température moyenne air (°C) | Chaleur → Prise/propagation feu |
| `relative_humidity` | Humidité relative air (%) | Air sec → Prise/intensité rapide |
| `wind_speed` | Vitesse du vent (m/s) | Oxygène & propagation spatiale |
| `landcover` | Classe occupation sol (ESA) | Filtre de contexte (Forêt vs Ferme) |
| `slope_deg` | Pente du terrain (NASADEM) | La pente accélère la propagation |
| `ndvi_10m` | Végétation -10j (Sentinel-2) | Combustible sec = risque élevé (10m) |
| `is_recent_loss` | Perte forestière (Hansen GFC) | 1 = Déforestation récente (indique brûlis/Tavy massif) |

> [!important] Architecture Hybride (Token + GEE)
> - **NASA Earthdata Token (`earthaccess`)** : Toujours utilisé pour télécharger massivement des archives HDF4 (MOD14A1) pour l'entraînement sur 2021-2024.
> - **Google Earth Engine (GEE)** : Spécifiquement utilisé pour l'extraction contextuelle en temps réel. Il évite de télécharger des images Sentinel-2 ou Hansen de plusieurs Go : il "pique" directement les valeurs au niveau du point FIRMS.

### Exemple Extraction GEE (Service)

```python
import ee
ee.Initialize()

def get_gee_features_batch(df):
    """Extrait météo (ERA5), sol, pente et NDVI par batch."""
    # (Voir implémentation détaillée dans le guide d'intégration)
    pass
```

---

## Pipeline Complet Feature Engineering

```python
# ml/preprocessing/feature_engineering.py

# ★ SCHEMA OFFICIEL : 20 Features
FEATURE_COLS = [
    # 1. Groupe FIRMS
    'diff_brightness', 'frp_log', 'brightness',
    'local_hour', 'is_dry_season', 'daynight_bin',
    'confidence_num', 'scan_track_ratio',
    # 2. Groupe HDBSCAN
    'cluster_size', 'cluster_frp_total', 'cluster_frp_max', 'is_noise',
    # 3. Groupe Météo & Contexte (GEE)
    'temperature_2m', 'relative_humidity', 'wind_speed',
    'landcover', 'slope_deg', 
    'ndvi_10m', 'is_recent_loss'   # V2 Sentinel-2 + Hansen
]

def build_features(df):
    # 1. Base FIRMS
    df['diff_brightness'] = df['brightness'] - df['bright_t31']
    df['frp_log'] = np.log1p(df['frp'])
    df['local_hour'] = (df['acq_time'] // 100 + 3) % 24
    df['is_dry_season'] = df['month'].isin([4,5,6,7,8,9,10]).astype(int)
    df['daynight_bin'] = (df['daynight'] == 'D').astype(int)
    df['confidence_num'] = df['confidence'].map({'high':90,'nominal':65,'low':30}).fillna(65)
    df['scan_track_ratio'] = df['scan'] / df['track'].replace(0, 1)
    df['is_noise'] = (df['cluster_id'] == -1).astype(int)
    
    # 2. Enrichissement Intelligent GEE
    # df = get_gee_features_batch(df) # (Injection Landcover/Slope/Sentinel2/Hansen)
    
    return df.fillna(0)
```

---

*JeryMotroNet → [[04_JeryMotroNet]]*
*HDBSCAN → [[05_HDBSCAN_Clustering]]*
