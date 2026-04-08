# 📡 APIs & Sources de Données — FireProject
#FireProject #API #NASA #FIRMS #MODIS #VIIRS #Sentinel2 #Dataset
[[Glossaire_Tags]] | [[00_INDEX]]

---

## 1. NASA FIRMS API (PRIORITÉ 1)

**Lien :** https://firms.modaps.eosdis.nasa.gov/api/area
**Référence complète :** [[REF-001_NASA_FIRMS_API]]
**Authentification :** MAP_KEY gratuite (inscription NASA Earthdata)

### 1.1 Endpoint principal

```
GET /api/area/csv/{MAP_KEY}/{SOURCE}/{BBOX}/{DAY_RANGE}
GET /api/area/csv/{MAP_KEY}/{SOURCE}/{BBOX}/{DAY_RANGE}/{DATE}
```

### 1.2 Sources disponibles pour Madagascar

| SOURCE | Capteur | Résolution | Fréquence |
|--------|---------|------------|-----------|
| `MODIS_NRT` | MODIS Terra/Aqua | 1km | ~3h |
| `MODIS_SP` | MODIS (archive) | 1km | Historique |
| `VIIRS_SNPP_NRT` | VIIRS S-NPP | 375m | ~1.5h |
| `VIIRS_NOAA20_NRT` | VIIRS NOAA-20 | 375m | ~1.5h |
| `VIIRS_NOAA21_NRT` | VIIRS NOAA-21 | 375m | ~1.5h |
| `VIIRS_SNPP_SP` | VIIRS (archive) | 375m | Historique |

> **Recommandation FireProject :** Utiliser `VIIRS_SNPP_NRT` en priorité (meilleure résolution), puis `MODIS_NRT` en complément.

### 1.3 Bounding Box Madagascar

```
43.0,-25.6,50.5,-11.9
```

→ west=43.0, south=-25.6, east=50.5, north=-11.9

### 1.4 Exemples d'appels

```python
import requests

MAP_KEY = "VOTRE_MAP_KEY"
BBOX = "43.0,-25.6,50.5,-11.9"

# VIIRS dernières 24h
url = f"https://firms.modaps.eosdis.nasa.gov/api/area/csv/{MAP_KEY}/VIIRS_SNPP_NRT/{BBOX}/1"

# MODIS sur une semaine depuis une date
url = f"https://firms.modaps.eosdis.nasa.gov/api/area/csv/{MAP_KEY}/MODIS_NRT/{BBOX}/7/2025-06-01"

response = requests.get(url)
with open("data/raw/firms/firms_today.csv", "w") as f:
    f.write(response.text)
```

### 1.5 Colonnes importantes du CSV FIRMS

| Colonne | Type | Description | Usage ML |
|---------|------|-------------|----------|
| `latitude` | float | Position GPS | Feature spatiale |
| `longitude` | float | Position GPS | Feature spatiale |
| `brightness` | float | Temp. brillance (K) | Feature principale |
| `frp` | float | Fire Radiative Power (MW) | Feature intensité |
| `confidence` | int/str | Niveau confiance (%) | Filtre qualité |
| `acq_date` | date | Date acquisition | Feature temporelle |
| `acq_time` | time | Heure acquisition | Feature temporelle |
| `daynight` | char | D (jour) / N (nuit) | Feature booléenne |
| `satellite` | str | Nom du satellite | Feature source |

### 1.6 Filtrage recommandé

```python
import pandas as pd

df = pd.read_csv("firms_today.csv")

# Filtrer confiance minimum
df_filtered = df[df['confidence'] >= 30]

# Filtrer FRP significatif
df_filtered = df_filtered[df_filtered['frp'] >= 5.0]

# Supprimer doublons (même position à moins de 500m)
# (utiliser GeoPandas pour distance spatiale)
```

---

## 2. NASA EARTHDATA API (DONNÉES CLIMATIQUES & ARCHIVES)

**Lien :** https://earthdata.nasa.gov
**Authentification :** Token JWT (gratuit)

```
Token actuel : eyJ0eXAiOiJKV1QiLCJvcmlnaW4iO...
⚠️ NE PAS PARTAGER CE TOKEN — valide jusqu'à ~2025-05-XX
```

### 2.1 Produits utiles pour Madagascar

| Produit | Description | Format |
|---------|-------------|--------|
| MOD13A2 | NDVI MODIS 16 jours (1km) | HDF4 |
| MOD14A1 | Détection feux quotidienne | HDF4 |
| MYD14A1 | Détection feux Aqua quotidienne | HDF4 |
| MOD09GA | Réflectance surface quotidienne | HDF4 |

### 2.2 Accès via earthaccess (Python)

```python
import earthaccess

earthaccess.login(strategy="token", token="VOTRE_TOKEN")

results = earthaccess.search_data(
    short_name="MOD14A1",
    temporal=("2024-01-01", "2024-12-31"),
    bounding_box=(43.0, -25.6, 50.5, -11.9)
)

earthaccess.download(results, "data/raw/modis/")
```

---

## 3. COPERNICUS SENTINEL HUB (ESA)

**Lien :** https://shapps.dataspace.copernicus.eu/dhus/
**Authentification :** Compte Copernicus gratuit
**Référence :** [[REF-003_Copernicus_Sentinel]]

### 3.1 Sentinel-2 (Optique — Feux & Déforestation)

| Paramètre | Valeur |
|-----------|--------|
| Résolution | 10m (B02,B03,B04,B08) / 20m (B11,B12) |
| Revisite | 5 jours (combiné S2A + S2B) |
| Nuages | Problème majeur (saison des pluies) |
| Bandes clés | B04 (Rouge), B08 (NIR), B11 (SWIR), B12 (SWIR2) |

**Indices calculés :**
```python
import numpy as np

# NDVI : végétation (forêt intacte = proche de 1)
NDVI = (B08 - B04) / (B08 + B04)

# NBR : zones brûlées (cicatrices = très négatif)
NBR = (B08 - B12) / (B08 + B12)

# dNBR : différence avant/après feu (sévérité du brûlage)
dNBR = NBR_avant - NBR_apres
```

### 3.2 Sentinel-1 (SAR — Tout temps, nuit incluse)

> ⚡ **Avantage majeur** : Pénètre les nuages — résout PROB-002 !

| Paramètre | Valeur |
|-----------|--------|
| Type | Radar à ouverture synthétique (SAR) |
| Résolution | 10m |
| Revisite | 6–12 jours |
| Usage | Détection changements forestiers même sous nuages |

### 3.3 Accès via sentinelhub-py

```python
from sentinelhub import SHConfig, BBox, CRS, DataCollection, SentinelHubRequest

config = SHConfig()
config.instance_id = "VOTRE_INSTANCE_ID"

bbox = BBox(bbox=[43.0, -25.6, 50.5, -11.9], crs=CRS.WGS84)

request = SentinelHubRequest(
    data_folder="data/raw/sentinel2/",
    evalscript="""...""",  # Script de sélection des bandes
    input_data=[SentinelHubRequest.input_data(
        data_collection=DataCollection.SENTINEL2_L2A,
        time_interval=("2024-06-01", "2024-06-30"),
    )],
    responses=[SentinelHubRequest.output_response("default", MimeType.TIFF)],
    bbox=bbox,
    size=[512, 512],
    config=config,
)
```

---

## 4. HANSEN GLOBAL FOREST CHANGE

**Lien :** https://earthenginepartners.appspot.com/science-2013-global-forest
**Accès :** Google Earth Engine (gratuit) ou téléchargement direct

### 4.1 Couches disponibles

| Couche | Description | Usage |
|--------|-------------|-------|
| `treecover2000` | Couverture forestière 2000 (%) | Référence de base |
| `loss` | Perte forestière (1 = perte) | Feature déforestation |
| `lossyear` | Année de la perte (0–23) | Chronologie |
| `gain` | Gain forestier 2000–2012 | Feature secondaire |

### 4.2 Via Google Earth Engine (Python)

```python
import ee
ee.Initialize()

dataset = ee.Image("UMD/hansen/global_forest_change_2023_v1_11")
lossImage = dataset.select("loss")
lossYear = dataset.select("lossyear")

# Export pour Madagascar
task = ee.batch.Export.image.toDrive(
    image=lossImage,
    description="madagascar_forest_loss",
    region=ee.Geometry.BBox(43.0, -25.6, 50.5, -11.9),
    scale=30,
    fileFormat="GeoTIFF"
)
task.start()
```

---

## 5. AFIS (African Fire Information System)

**Lien :** https://www.afis.co.za/afisalert/
**Référence :** [[REF-002_AFIS_System]]
**Statut :** Optionnel (contact nécessaire pour API)

> Système africain complémentaire — à contacter pour partenariat.

---

## 6. TABLEAU RÉCAPITULATIF DES SOURCES

| Source | Type | Résolution | Fréquence | Coût | Priorité |
|--------|------|------------|-----------|------|----------|
| FIRMS VIIRS NRT | Thermique | 375m | ~1.5h | Gratuit | 🔴 P1 |
| FIRMS MODIS NRT | Thermique | 1km | ~3h | Gratuit | 🔴 P1 |
| Sentinel-2 | Optique | 10m | 5 jours | Gratuit | 🔴 P1 |
| Hansen GFC | Déforestation | 30m | Annuel | Gratuit | 🟠 P2 |
| Sentinel-1 SAR | Radar | 10m | 6–12j | Gratuit | 🟠 P2 |
| NASA Earthdata | Climatique | Variable | Variable | Gratuit | 🟡 P3 |
| AFIS | Thermique Afrique | Variable | Variable | Contact | 🟡 P3 |

---

*Dataset MODIS → [[08_Dataset_FIRMS_MODIS]]*
*Dataset VIIRS → [[08_Dataset_FIRMS_VIIRS]]*
*Dataset Sentinel-2 → [[08_Dataset_Sentinel2]]*
*Architecture → [[04_Architecture_Globale]]*
