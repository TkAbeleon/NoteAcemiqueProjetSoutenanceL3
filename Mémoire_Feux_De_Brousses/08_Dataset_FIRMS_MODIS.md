# 📊 Dataset — FIRMS MODIS
#FireProject #Dataset #NASA #MODIS #DataCleaning #Satellite
[[Glossaire_Tags]] | [[05_APIs_et_Donnees]] | [[00_INDEX]]

---

## Métadonnées du Dataset

| Champ | Valeur |
|-------|--------|
| **Nom** | FIRMS MODIS NRT — Madagascar |
| **Source** | NASA FIRMS |
| **Capteur** | MODIS Terra + Aqua |
| **Résolution spatiale** | ~1km × 1km |
| **Zone** | Madagascar (43.0,-25.6,50.5,-11.9) |
| **Période couverte** | 2020–2024 (archive) + quotidien (NRT) |
| **Format** | CSV |
| **Lien** | https://firms.modaps.eosdis.nasa.gov/api/area |
| **Coût** | Gratuit (MAP_KEY gratuite) |

---

## Colonnes du Dataset

| Colonne | Type | Plage valeurs | Usage ML |
|---------|------|---------------|----------|
| `latitude` | float | -25.6 → -11.9 | Feature spatiale |
| `longitude` | float | 43.0 → 50.5 | Feature spatiale |
| `brightness` | float | 300–500 K | Feature principale |
| `scan` | float | 1.0–5.0 km | Feature qualité |
| `track` | float | 1.0–5.0 km | Feature qualité |
| `acq_date` | date | YYYY-MM-DD | Feature temporelle |
| `acq_time` | int | 0000–2359 | Feature temporelle |
| `satellite` | str | T, A | Feature source |
| `instrument` | str | MODIS | Métadonnée |
| `confidence` | int | 0–100 | Filtre qualité |
| `version` | str | 6.1NRT | Métadonnée |
| `bright_t31` | float | 270–350 K | Feature thermique |
| `frp` | float | 0–1000+ MW | Feature intensité |
| `daynight` | char | D, N | Feature booléenne |

---

## Statistiques descriptives (estimées — Madagascar 2024)

| Métrique | Valeur attendue |
|----------|----------------|
| Nb détections/an | ~15 000–50 000 |
| FRP médian | ~30–50 MW |
| FRP max (pic saison sèche) | > 500 MW |
| Confiance moyenne | ~65% |
| % feux nocturnes | ~35% |
| Pic mensuel | Septembre–Octobre |

---

## Commandes de téléchargement

```python
import requests, os

MAP_KEY = "VOTRE_MAP_KEY"
BBOX = "43.0,-25.6,50.5,-11.9"
OUTPUT_DIR = "data/raw/firms/modis/"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Archive : télécharger par mois (2020–2024)
for year in range(2020, 2025):
    for month in range(1, 13):
        date_str = f"{year}-{month:02d}-01"
        url = f"https://firms.modaps.eosdis.nasa.gov/api/area/csv/{MAP_KEY}/MODIS_NRT/{BBOX}/30/{date_str}"
        response = requests.get(url, timeout=60)
        filename = f"{OUTPUT_DIR}modis_{year}_{month:02d}.csv"
        with open(filename, "w") as f:
            f.write(response.text)
        print(f"✅ Téléchargé : {filename} ({len(response.text)} bytes)")
```

---

## Notes de Nettoyage

- Filtrer `confidence >= 30` (exclure détections non fiables)
- Filtrer `frp >= 1.0` (exclure bruit thermique)
- Supprimer doublons spatiotemporels (même position ± 0.01° à ± 1h)
- Vérifier les valeurs aberrantes : `brightness > 500K` = erreur capteur probable
- Ajouter colonne `source = 'MODIS'` avant fusion avec VIIRS

---

## Liens croisés

- Dataset VIIRS → [[08_Dataset_FIRMS_VIIRS]]
- API documentation → [[REF-001_NASA_FIRMS_API]]
- Preprocessing → [[06_Pipeline_ML_DL]]
