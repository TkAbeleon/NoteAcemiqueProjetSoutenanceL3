# Pipeline de données

```
Boucle FastAPI
  ↓
Collecte FIRMS
  ↓
Normalisation
  ↓
Validation géographique
  ↓
Région
  ↓
Scoring ML / fallback
  ↓
HDBSCAN / fallback grille
  ↓
FireEvent
  ↓
Statut + alertes
```

## Collecte
Le service de collecte interroge l'API FIRMS avec une bbox de Madagascar et les sources configurées. Il gère les fenêtres disponibles et la complétude.

## Normalisation
Le code calcule notamment `diff_brightness`, `frp_log`, `scan_track_ratio`, `local_hour` et `is_dry_season`.

## Déduplication
La table `firms_fire_detections` possède une contrainte unique sur latitude, longitude, date, heure, satellite et instrument.

## Ordre
L'étiquetage régional a lieu avant le scoring et le clustering dans le pipeline automatique.

## GEE
L'enrichissement environnemental n'est pas une étape synchronisée dans `run_automatic_pipeline()`. Il doit être documenté comme pipeline séparé.

## Limite
Un pipeline automatique disponible dans le code ne signifie pas qu'il est toujours exécuté avec succès : il dépend des services, secrets, réseau et base.