# Enrichissement environnemental Google Earth Engine

## Position
Le projet contient plusieurs scripts GEE, notamment `Backend/data/gee_enrich_firms.py` et `Backend/data/GEE_ENRICH/main.py`.

## Entrée
Le script Colab charge via KaggleHub le dataset public `tsikynyantsa/firms-nasa`, fichier `FIRMS.csv`.

## Variables produites
- température ;
- humidité relative ;
- vitesse du vent ;
- couverture du sol ;
- pente ;
- NDVI ;
- perte forestière récente.

## Sources visibles dans le code
- NASADEM pour la pente ;
- ESA WorldCover pour landcover ;
- Hansen Global Forest Change 2025 pour `is_recent_loss` ;
- ERA5-Land pour température, point de rosée et vent ;
- MODIS MOD13A2 pour NDVI.

## Calculs
Le script convertit la température de Kelvin en Celsius, estime l'humidité relative et calcule la vitesse du vent avec les composantes u/v. Le NDVI MODIS est remis à l'échelle.

## Batch
Le script Colab traite par lots de 500 lignes par défaut et permet une reprise depuis le fichier de sortie.

## Distinction essentielle
`run_automatic_pipeline()` n'appelle pas le worker GEE. L'enrichissement est donc documenté comme traitement séparé.

## Déforestation
`is_recent_loss` est un contexte de perte forestière récente. Il ne faut pas le transformer en affirmation de détection autonome complète de la déforestation.

---

**Navigation :** [[08_CLUSTERING_ET_SUIVI_DES_FEUX|← Précédent]] | [[00_INDEX|Index]] | [[10_STATISTIQUES_ET_ANALYSE|Suivant →]]
