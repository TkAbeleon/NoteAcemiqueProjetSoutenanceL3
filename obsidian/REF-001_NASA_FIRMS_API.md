# 📚 REF-001 — NASA FIRMS API
#JeryMotro #Reference #API #NASA #FIRMS #Documentation
[[Glossaire_Tags]] | [[00_INDEX]]

| Champ | Valeur |
|-------|--------|
| **Lien** | https://firms.modaps.eosdis.nasa.gov/api/area |
| **Type** | Documentation API REST officielle |
| **Accès** | MAP_KEY gratuite (inscription earthdata.nasa.gov) |

## Endpoints principaux pour JeryMotro

```
# VIIRS SNPP NRT — dernière heure
GET /api/area/csv/{MAP_KEY}/VIIRS_SNPP_NRT/-25.5,43,-11.5,50/1

# VIIRS NOAA21 NRT
GET /api/area/csv/{MAP_KEY}/VIIRS_NOAA21_NRT/-25.5,43,-11.5,50/1

# MODIS NRT — dernière heure
GET /api/area/csv/{MAP_KEY}/MODIS_NRT/-25.5,43,-11.5,50/1

# Archives MODIS (par mois)
GET /api/area/csv/{MAP_KEY}/MODIS_SP/-25.5,43,-11.5,50/30/2024-06-01
```

## Notes importantes
- DAY_RANGE max = 10 jours par appel
- MAP_KEY = 40 chars alphanum — jamais dans le code → `.env`
- RT/URT = temporaires, remplacés par NRT après traitement
