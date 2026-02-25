# 📊 Dataset — FIRMS VIIRS SNPP
#FireProject #Dataset #NASA #VIIRS #DataCleaning #Satellite
[[Glossaire_Tags]] | [[05_APIs_et_Donnees]] | [[00_INDEX]]

---

## Métadonnées

| Champ | Valeur |
|-------|--------|
| **Nom** | FIRMS VIIRS SNPP NRT — Madagascar |
| **Source** | NASA FIRMS |
| **Capteur** | VIIRS Suomi-NPP |
| **Résolution spatiale** | 375m × 375m |
| **Zone** | Madagascar (43.0,-25.6,50.5,-11.9) |
| **Format** | CSV |
| **Lien** | https://firms.modaps.eosdis.nasa.gov |
| **Coût** | Gratuit |

---

## Différences clés vs MODIS

| Caractéristique | MODIS | VIIRS |
|----------------|-------|-------|
| Résolution spatiale | 1km | **375m** ← meilleure |
| Résolution thermique | Standard | **Améliorée** |
| Fréquence passage | ~3h | **~1.5h** ← plus fréquent |
| Colonnes | 14 | **15** (+ `bright_ti4`, `bright_ti5`) |
| Colonne confiance | Numérique 0–100 | **Catégorielle** : low/nominal/high |

---

## Colonnes spécifiques VIIRS

| Colonne | Description |
|---------|-------------|
| `bright_ti4` | Luminosité bande I4 (3.75μm) |
| `bright_ti5` | Luminosité bande I5 (11.45μm) — remplace bright_t31 |
| `confidence` | `low` / `nominal` / `high` (≠ MODIS numérique) |

---

## Gestion de la confiance VIIRS

```python
# Conversion confiance catégorielle → numérique pour ML
confidence_map = {'low': 30, 'nominal': 65, 'high': 90}
df['confidence_num'] = df['confidence'].map(confidence_map)

# Filtre recommandé
df_filtered = df[df['confidence'].isin(['nominal', 'high'])]
```

---

## Sources VIIRS disponibles

| Source API | Capteur | Priorité |
|-----------|---------|----------|
| `VIIRS_SNPP_NRT` | Suomi-NPP | 🔴 P1 |
| `VIIRS_NOAA20_NRT` | NOAA-20 (JPSS-1) | 🔴 P1 |
| `VIIRS_NOAA21_NRT` | NOAA-21 (JPSS-2) | 🟠 P2 |
| `VIIRS_SNPP_SP` | Archive SNPP | 🟡 Archive |

---

## Fusion MODIS + VIIRS

```python
import pandas as pd

def merge_modis_viirs(modis_df, viirs_df):
    """Fusionne MODIS et VIIRS en un dataset unifié."""

    # Standardiser colonnes VIIRS
    viirs_df['bright_t31'] = viirs_df['bright_ti5']
    viirs_df['confidence_num'] = viirs_df['confidence'].map(
        {'low': 30, 'nominal': 65, 'high': 90}
    )

    # Standardiser colonnes MODIS
    modis_df['confidence_num'] = modis_df['confidence']

    # Colonnes communes
    common_cols = ['latitude', 'longitude', 'brightness',
                   'frp', 'confidence_num', 'acq_date',
                   'acq_time', 'daynight', 'satellite', 'source']

    modis_df['source'] = 'MODIS'
    viirs_df['source'] = 'VIIRS'

    merged = pd.concat([
        modis_df[common_cols],
        viirs_df[common_cols]
    ], ignore_index=True)

    # Déduplication spatiotemporelle (500m, 2h)
    merged = merged.drop_duplicates(subset=[
        merged['latitude'].round(2),
        merged['longitude'].round(2),
        'acq_date'
    ])

    return merged
```
