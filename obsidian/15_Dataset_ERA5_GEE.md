# 🌤️ Dataset — ERA5 (Google Earth Engine)
#JeryMotro #Dataset #Python #ML #TimeSeries
[[Glossaire_Tags]] | [[00_INDEX]]

---

| Champ | Valeur |
|-------|--------|
| **Source** | ECMWF ERA5 via Google Earth Engine |
| **Produit GEE** | `ECMWF/ERA5/DAILY` |
| **Variables** | Température, humidité, vent, précipitations |
| **Résolution** | ~28km (suffisant pour features ML) |
| **Accès** | Compte GEE académique gratuit |

---

## Variables ERA5 utiles pour JeryMotroNet

| Variable GEE | Feature ML | Rôle |
|--------------|-----------|------|
| `mean_2m_air_temperature` | `temperature_2m` | Chaleur → risque feu |
| `dewpoint_2m_temperature` | → `relative_humidity` | Sécheresse → risque |
| `total_precipitation` | `precipitation_mm` | Pluie → éteint feu |
| `u_component_of_wind_10m` | → `wind_speed` | Propagation feu |
| `v_component_of_wind_10m` | → `wind_speed` | Propagation feu |

## Accès Python

```python
import ee
ee.Initialize()  # Compte GEE académique requis

# Dataset ERA5 journalier
era5 = ee.ImageCollection("ECMWF/ERA5/DAILY")

# Exemple : température 23/02/2026 pour Madagascar
image = era5.filterDate("2026-02-23", "2026-02-24").first()
```

---

*Feature Engineering → [[06_Feature_Engineering]]*
*JeryMotroNet → [[04_JeryMotroNet]]*
