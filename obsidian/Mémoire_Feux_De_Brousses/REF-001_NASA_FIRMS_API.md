# 📚 REF-001 — NASA FIRMS API
#FireProject #Reference #API #NASA #FIRMS #Documentation
[[Glossaire_Tags]] | [[05_APIs_et_Donnees]] | [[00_INDEX]]

---

## Métadonnées

| Champ | Valeur |
|-------|--------|
| **Titre** | API FIRMS — Area CSV |
| **Source** | NASA FIRMS |
| **Lien** | https://firms.modaps.eosdis.nasa.gov/api/area |
| **Type** | Documentation officielle API REST |
| **Accès** | MAP_KEY gratuite (inscription sur firms.modaps.eosdis.nasa.gov) |

---

## Résumé

API permettant de récupérer des données CSV de détection d'incendies par satellite (MODIS, VIIRS) sur une zone géographique définie, avec plage temporelle configurable.

---

## Endpoints

```
# Données récentes (depuis aujourd'hui)
GET /api/area/csv/{MAP_KEY}/{SOURCE}/{BBOX}/{DAY_RANGE}

# Données depuis une date
GET /api/area/csv/{MAP_KEY}/{SOURCE}/{BBOX}/{DAY_RANGE}/{DATE}

# Vérifier disponibilité
GET /api/data_availability/
```

---

## Exemples Complets

```python
# Feux Madagascar — dernières 24h (VIIRS)
url = "https://firms.modaps.eosdis.nasa.gov/api/area/csv/MAP_KEY/VIIRS_SNPP_NRT/43.0,-25.6,50.5,-11.9/1"

# Feux Madagascar — 7 jours depuis le 1er juin 2024
url = "https://firms.modaps.eosdis.nasa.gov/api/area/csv/MAP_KEY/MODIS_NRT/43.0,-25.6,50.5,-11.9/7/2024-06-01"

# Feux monde entier — dernières 24h
url = "https://firms.modaps.eosdis.nasa.gov/api/area/csv/MAP_KEY/VIIRS_SNPP_NRT/world/1"
```

---

## Notes Importantes

- DAY_RANGE max = 10 jours par appel
- Pour archives longues : boucler sur périodes mensuelles
- RT/URT (Real-Time) = données temporaires avant NRT
- MAP_KEY = 40 caractères alphanumériques, gratuite, illimitée

---

## Lien avec projet

- Utilisé dans : [[08_Dataset_FIRMS_MODIS]] | [[08_Dataset_FIRMS_VIIRS]]
- Intégré dans : [[07_Automatisation_n8n]] (workflow `daily_collection`)
