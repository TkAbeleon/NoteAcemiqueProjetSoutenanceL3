# FireProject — Référence API : FIRMS Area CSV

#Reference #Article #Tutoriel #API #Soutenance  
[[Glossaire_Tags]]

---

## Métadonnées

**Titre :** API FIRMS — Area CSV  
**Auteur / Source :** NASA FIRMS  
**Lien :** [https://firms.modaps.eosdis.nasa.gov/api/area](https://firms.modaps.eosdis.nasa.gov/api/area)  
**Résumé :** API permettant de récupérer des données de détection d’incendie satellite (LANDSAT, MODIS, VIIRS) sur une zone géographique donnée, avec plage de dates configurable.  
**Notes importantes :** Nécessite une MAP_KEY gratuite.

---

## Vue générale

Cette API permet d’extraire des données CSV de détection d’incendies sur une **zone définie**, pour une **source satellite**, et une **plage temporelle**.

---

## Endpoints

### Données récentes

```
/api/area/csv/[MAP_KEY]/[SOURCE]/[AREA_COORDINATES]/[DAY_RANGE]
```

→ Retourne les données de **aujourd’hui** jusqu’à `DAY_RANGE - 1`.

---

### Données à partir d’une date

```
/api/area/csv/[MAP_KEY]/[SOURCE]/[AREA_COORDINATES]/[DAY_RANGE]/[DATE]
```

→ Retourne les données de `[DATE]` jusqu’à `[DATE + DAY_RANGE - 1]`.

---

## Paramètres

### SOURCE

- `LANDSAT_NRT` — US/Canada uniquement
    
- `MODIS_NRT`
    
- `MODIS_SP`
    
- `VIIRS_NOAA20_NRT`
    
- `VIIRS_NOAA20_SP`
    
- `VIIRS_NOAA21_NRT`
    
- `VIIRS_SNPP_NRT`
    
- `VIIRS_SNPP_SP`
    

> RT/URT = données temps réel, remplacées par NRT après traitement.

---

### AREA_COORDINATES

Format :

```
west,south,east,north
```

Exemple :

```
-85,-57,-32,14
```

Ou :

```
world → [-180,-90,180,90]
```

---

### DAY_RANGE

```
1 → 5 jours
```

---

### DATE (optionnel)

```
YYYY-MM-DD
```

Si omis → données les plus récentes.

Vérification disponibilité :

```
/api/data_availability/
```

---

## MAP_KEY

Une clé gratuite est requise pour utiliser l’API.

Fonctions :

- Générer une MAP_KEY
    
- Vérifier les transactions disponibles
    

---

## Tables d’attributs (références)

- LANDSAT — table attributs
    
- MODIS — table attributs
    
- VIIRS S-NPP — table attributs
    
- VIIRS NOAA-20 — table attributs
    
- VIIRS NOAA-21 — table attributs
    

---

## Notes techniques

- Real-Time = données < 60 minutes après passage satellite
    
- Ultra Real-Time = quelques secondes après acquisition
    
- Les données RT/URT sont temporaires
    

---

## Exemple d’utilisation

```
/api/area/csv/KEY/MODIS_NRT/world/1
```

→ Télécharge les détections récentes mondiales.

---

## À retenir

✔ Zone = bounding box ou world  
✔ MAP_KEY obligatoire  
✔ CSV exploitable directement  
✔ Compatible automatisation / scripts

---

## Idées d’intégration FireProject

- Surveillance incendies Madagascar
    
- Dashboard temps réel
    
- Pipeline ML détection anomalies
    
- Automatisation n8n
    

---

**Tags suggérés :**  
#NASA #FIRMS #Satellite #Wildfire #API #CSV #DataPipeline

---