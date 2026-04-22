# 📅 Plan d'Exécution : Jour 1 & Jour 2 (Pipeline de Données)
#JeryMotro #Plan #DataEngineering #ML

Puisque tu possèdes **déjà les fichiers CSV complets de 2020 à aujourd'hui**, l'objectif immédiat n'est plus la collecte, mais la préparation de ces données pour le Machine Learning. 

Voici un plan de frappe réaliste, découpé en sessions très concentrées de **1h30 par jour maximum**.

---

## 🟢 AUJOURD'HUI (Jour 1) : Nettoyage et Features de Base (1h30)
*L'objectif du jour est de prendre tous tes CSV disparates, d'en faire un seul gros dataset propre, et de créer les premières features spatio-temporelles.*

### ⏱️ Étape 1 : Fusion & Nettoyage (30 mins)
1. Créer un notebook Colab/Jupyter : `02_Feature_Engineering.ipynb`.
2. Charger tous les CSV de 2020 à "maintenant" dans un seul gros `DataFrame` Pandas.
3. Supprimer les doublons exacts (`drop_duplicates()`).
4. Filtrer les données inutiles (ex: `confidence < 30` ou les anomalies évidentes).
5. Convertir `acq_date` et `acq_time` en un objet DateTime (très important pour les séries temporelles plus tard).

```python
import glob, pandas as pd

files = glob.glob("data/raw/firms/*.csv") 
df = pd.concat([pd.read_csv(f) for f in files], ignore_index=True)
df.drop_duplicates(inplace=True)
df = df[df['confidence'] >= 30]
df['datetime'] = pd.to_datetime(df['acq_date']) + pd.to_timedelta(df['acq_time'].astype(str).str.zfill(4).str[:2] + ':' + df['acq_time'].astype(str).str.zfill(4).str[2:] + ':00')
```

### ⏱️ Étape 2 : Création des 8 Features FIRMS (30 mins)
1. Calculer `diff_brightness` = `brightness - bright_t31`.
2. Calculer `frp_log` = `np.log1p(frp)`.
3. Calculer `local_hour` en convertissant l'heure UTC en EAT (UTC+3).
4. Créer la variable booléenne `is_dry_season`.
5. Mapper la confiance `nominal/high/low` en valeurs numériques `65, 90, 30`.

```python
import numpy as np

df['diff_brightness'] = df['brightness'] - df['bright_t31']
df['frp_log'] = np.log1p(df['frp'])
df['local_hour'] = (df['acq_time'] // 100 + 3) % 24
df['month'] = pd.to_datetime(df['acq_date']).dt.month
df['is_dry_season'] = df['month'].isin(range(4, 11)).astype(int)
df['confidence_num'] = df['confidence'].map({'high': 90, 'nominal': 65, 'low': 30}).fillna(65)
df['scan_track_ratio'] = df['scan'] / df['track'].replace(0, 1)
```

### ⏱️ Étape 3 : Clustering Spatial HDBSCAN (30 mins)
1. Isoler les colonnes `latitude`, `longitude`.
2. Faire tourner HDBSCAN sur des groupes par jour (pour ne pas saturer la RAM).
3. Assigner `cluster_id`, calculer `cluster_size` et `is_noise`.
4. Calculer le FRP total et max du cluster.
5. **Sauvegarder** : `df_firms_hdbscan_2020_2026.parquet` (préférer `.parquet` au CSV pour ce volume).

```python
from hdbscan import HDBSCAN

# ⚠️ Grouper par jour pour éviter de saturer la RAM
for date, group in df.groupby('acq_date'):
    coords = group[['latitude', 'longitude']].values
    labels = HDBSCAN(min_cluster_size=3, min_samples=1).fit_predict(coords)
    df.loc[group.index, 'cluster_id'] = labels

df['is_noise'] = (df['cluster_id'] == -1).astype(int)
agg = df.groupby('cluster_id')['frp'].agg(cluster_size='count', cluster_frp_total='sum', cluster_frp_max='max')
df = df.merge(agg, on='cluster_id', how='left')
df.to_parquet("df_firms_hdbscan.parquet", index=False)
```

---

## 🔵 DEMAIN (Jour 2) : Enrichissement GEE & Labellisation (1h30)
*L'objectif est d'ajouter l'intelligence métier environnementale via Google Earth Engine et de générer la variable cible (Y) que le XGBoost devra deviner.*

### ⏱️ Étape 1 : Connexion GEE & Test unitaire (30 mins)
1. Vérifier que tu es loggé (`ee.Authenticate()`).
2. Écrire une petite fonction qui teste 1 seul point (lat, lon, date).

```python
import ee
ee.Initialize()

def get_context(lat, lon, date_str):
    pt = ee.Geometry.Point([lon, lat])
    d  = ee.Date(date_str)
    
    # Hansen GFC
    hansen  = ee.Image("UMD/hansen/global_forest_change_2023_v1_11")
    loss    = hansen.select('loss').reduceRegion(ee.Reducer.first(), pt, 30).getInfo()
    
    # ESA Landcover
    lc = ee.ImageCollection('ESA/WorldCover/v200').first()
    lc_val = lc.select('Map').reduceRegion(ee.Reducer.first(), pt, 10).getInfo()

    return {'is_recent_loss': loss.get('loss'), 'landcover': lc_val.get('Map')}

# Test sur 1 point
print(get_context(-20.1, 44.3, '2024-08-15'))
```

### ⏱️ Étape 2 : Extraction par Batch GEE (40 mins)
1. Recharger le fichier parquet d'hier.
2. **IMPORTANT :** tester sur 5000 feux seulement (`df.sample(5000)`).
3. Appliquer `get_context()` sur chaque ligne avec `apply()`.

```python
df_sample = pd.read_parquet("df_firms_hdbscan.parquet").sample(5000, random_state=42)

# Appliquer fonction GEE sur chaque ligne (peut prendre 15-20 min)
results = df_sample.apply(
    lambda r: get_context(r['latitude'], r['longitude'], r['acq_date']), axis=1
)
df_enriched = df_sample.join(pd.json_normalize(results))
df_enriched.to_parquet("df_sample_enriched.parquet")
```

> ⚠️ Si GEE plante pour des centaines de requêtes → utiliser `time.sleep(0.1)` entre chaque appel.

### ⏱️ Étape 3 : Scorage Heuristique (Label) (20 mins)
1. Appliquer la logique de labellisation heuristique vue dans `04_MadFireNet.md`.

```python
df_enriched['fire_label'] = 0

# Feu fortement confirmé
df_enriched.loc[(df_enriched['confidence_num'] >= 85) & (df_enriched['frp'] > 15), 'fire_label'] = 1

# Feu probable (brûlis agricole / Tavy)
df_enriched.loc[
    (df_enriched['confidence_num'] >= 60) & (df_enriched['frp'] > 8) &
    (df_enriched['is_dry_season'] == 1) & (df_enriched['is_recent_loss'] == 1),
    'fire_label'
] = 1

print(df_enriched['fire_label'].value_counts())
df_enriched.to_parquet("JeryMotro_Train_READY.parquet")
```

---

**Résultat attendu en 48h (3 heures de travail total) :**
Tu passeras de "simples données brutes réparties dans plusieurs CSV" à un "Dataset d'Entraînement 100% prêt à être digéré par le modèle XGBoost".

---

## 📦 LIVRABLES À PRODUIRE

### ✅ Fin Jour 1 — 2 fichiers

| Livrable | Description |
|----------|-------------|
| `02_Feature_Engineering.ipynb` | Notebook propre avec toutes les étapes (fusion, nettoyage, features FIRMS, HDBSCAN) |
| `df_firms_hdbscan.parquet` | Dataset complet 2020-2026 avec les 8 features FIRMS + `cluster_id`, `cluster_size`, `is_noise` |

### ✅ Fin Jour 2 — 2 fichiers

| Livrable | Description |
|----------|-------------|
| `gee_enrichment.py` | Script Python autonome avec la fonction `get_context(lat, lon, date)` validée |
| `JeryMotro_Train_READY.parquet` | Échantillon 5000 feux **100% prêt à entraîner XGBoost** (20 features + `fire_label`) |

---

## 🔍 CRITÈRE DE VALIDATION

Ton dataset est valide si ce bloc passe sans erreur :

```python
df = pd.read_parquet("JeryMotro_Train_READY.parquet")

assert df.shape[1] == 21, "Manque des colonnes !"
assert df['fire_label'].nunique() == 2, "Label Y absent ou mono-classe !"
assert df.isnull().mean().max() < 0.10, "Trop de valeurs manquantes !"

print("✅ Dataset validé :", df.shape)
print(df['fire_label'].value_counts(normalize=True).round(2))
```

**Sortie attendue :**
```
✅ Dataset validé : (5000, 21)
0    0.80
1    0.20
```
