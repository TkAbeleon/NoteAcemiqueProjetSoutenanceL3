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

## Features ERA5 (Google Earth Engine)

```python
import ee
ee.Initialize()

def get_era5_features(date_str, lat, lon):
    """Récupère features météo ERA5 pour un point/date."""
    date = ee.Date(date_str)
    era5 = ee.ImageCollection("ECMWF/ERA5/DAILY") \
        .filterDate(date, date.advance(1, 'day')) \
        .first()

    point = ee.Geometry.Point([lon, lat])
    values = era5.select([
        'mean_2m_air_temperature',
        'minimum_2m_air_temperature',
        'total_precipitation',
        'u_component_of_wind_10m',
        'v_component_of_wind_10m'
    ]).sample(point, 25000).first().toDictionary()

    return values.getInfo()
```

---

## Pipeline Complet Feature Engineering

```python
# ml/preprocessing/feature_engineering.py

FEATURE_COLS = [
    'diff_brightness', 'frp_log', 'brightness',
    'local_hour', 'is_dry_season', 'daynight_bin',
    'confidence_num', 'scan_track_ratio',
    'cluster_size', 'cluster_frp_total', 'cluster_frp_max', 'is_noise',
    'temperature_2m', 'relative_humidity', 'wind_speed'
]

def build_features(df):
    df['diff_brightness'] = df['brightness'] - df['bright_t31']
    df['frp_log'] = np.log1p(df['frp'])
    df['local_hour'] = (df['acq_time'] // 100 + 3) % 24
    df['is_dry_season'] = df['month'].isin([4,5,6,7,8,9,10]).astype(int)
    df['daynight_bin'] = (df['daynight'] == 'D').astype(int)
    df['confidence_num'] = df['confidence'].map({'high':90,'nominal':65,'low':30}).fillna(65)
    df['scan_track_ratio'] = df['scan'] / df['track'].replace(0, 1)
    df['is_noise'] = (df['cluster_id'] == -1).astype(int)
    return df.fillna(0)
```

---

*JeryMotroNet → [[04_JeryMotroNet]]*
*HDBSCAN → [[05_HDBSCAN_Clustering]]*
