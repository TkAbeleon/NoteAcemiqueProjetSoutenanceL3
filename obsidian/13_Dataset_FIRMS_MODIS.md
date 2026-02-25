# 📊 Dataset — FIRMS MODIS NRT
#JeryMotro #Dataset #NASA #MODIS #DataCleaning #Satellite
[[Glossaire_Tags]] | [[00_INDEX]]

---

| Champ | Valeur |
|-------|--------|
| **Nom** | FIRMS MODIS NRT — Madagascar |
| **Source** | NASA FIRMS |
| **Résolution** | ~1km |
| **Bbox** | `-25.5,43,-11.5,50` |
| **Période** | Archives 2020–2025 + NRT quotidien |
| **Format** | CSV |
| **API** | `MODIS_NRT` + `MODIS_SP` (archives) |
| **Coût** | Gratuit (MAP_KEY) |

---

## Colonnes

| Colonne | Type | Plage | Usage |
|---------|------|-------|-------|
| `latitude` | float | -25.5 → -11.5 | Spatial |
| `longitude` | float | 43 → 50.5 | Spatial |
| `brightness` | float | 300–500 K | Feature principale |
| `bright_t31` | float | 270–350 K | diff_brightness |
| `frp` | float | 0–1000+ MW | Intensité feu |
| `confidence` | int | 0–100 | Filtre qualité |
| `acq_date` | date | YYYY-MM-DD | Temporel |
| `acq_time` | int | 0000–2359 | Heure local |
| `daynight` | char | D / N | Feature |

## Commande de téléchargement

```python
# Archives par mois (loop 2020–2025)
url = f"https://firms.modaps.eosdis.nasa.gov/api/area/csv/{MAP_KEY}/MODIS_SP/-25.5,43,-11.5,50/30/{year}-{month:02d}-01"
```

---

*Dataset VIIRS → [[14_Dataset_FIRMS_VIIRS]]*
*API FIRMS → [[REF-001_NASA_FIRMS_API]]*
