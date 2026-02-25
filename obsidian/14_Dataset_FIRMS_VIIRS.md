# 📊 Dataset — FIRMS VIIRS SNPP + NOAA21
#JeryMotro #Dataset #NASA #VIIRS #DataCleaning #Satellite
[[Glossaire_Tags]] | [[00_INDEX]]

---

| Champ | Valeur |
|-------|--------|
| **Sources** | `VIIRS_SNPP_NRT` + `VIIRS_NOAA21_NRT` |
| **Résolution** | 375m (supérieure à MODIS 1km) |
| **Fréquence passage** | ~1.5h (SNPP) + ~1.5h (NOAA21) = quasi-continu |
| **Confiance** | Catégorielle : `low` / `nominal` / `high` |

---

## Différence clé vs MODIS

| | MODIS | VIIRS |
|--|-------|-------|
| Résolution | 1km | **375m** ← meilleure |
| Confiance | Numérique 0–100 | **Catégorielle** low/nominal/high |
| Colonne temp | `brightness` + `bright_t31` | `brightness` + `bright_ti5` |
| Fréquence | ~3h | **~1.5h** |

## Conversion confiance VIIRS → numérique

```python
confidence_map = {'low': 30, 'nominal': 65, 'high': 90}
df['confidence_num'] = df['confidence'].map(confidence_map)
```

## Filtre recommandé

```python
df = df[df['confidence'].isin(['nominal', 'high'])]  # Exclure low
df = df[df['frp'] >= 1.0]                             # Exclure bruit
```

---

*Dataset MODIS → [[13_Dataset_FIRMS_MODIS]]*
