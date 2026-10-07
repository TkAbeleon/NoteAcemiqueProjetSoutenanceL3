# Données FIRMS et base de données

## Table principale
`firms_fire_detections`, modèle `FirmsFireDetection`.

## Détection
Champs principaux :
- source, satellite, instrument ;
- latitude, longitude ;
- acq_date, acq_time, acq_datetime, local_hour ;
- brightness, bright_t31, diff_brightness ;
- frp, frp_log ;
- confidence, confidence_num ;
- daynight, scan, track, scan_track_ratio ;
- is_dry_season.

## Contexte environnemental
- temperature_2m ;
- relative_humidity ;
- wind_speed ;
- precipitation ;
- landcover ;
- fire_context_type ;
- context_percentages ;
- slope_deg ;
- ndvi_10m ;
- is_recent_loss.

## Analyse
- risk_score ;
- fire_label ;
- cluster_id ;
- fire_event_id ;
- cluster_size ;
- cluster_frp_total ;
- cluster_frp_max ;
- is_noise ;
- region ;
- collection_run_id.

## Relations importantes
`fire_event_id` est une vraie FK vers `fire_events.id`.

`collection_run_id` est une chaîne et n'est pas déclarée comme FK vers `CollectionRun`.

## Unicité
Une contrainte protège les doublons logiques : latitude + longitude + date + heure + satellite + instrument.

## Prediction
L'entité Prediction est distincte. Ne pas inventer une FK avec User, FireEvent ou FirmsFireDetection si elle n'existe pas.

## Base de production
La localisation actuelle de la base doit venir de `DATABASE_URL`. L'ancienne documentation qui parlait d'un PostgreSQL local ne doit pas être reprise comme fait actuel.

---

**Navigation :** [[04_PIPELINE_DONNEES|← Précédent]] | [[00_INDEX|Index]] | [[06_GEOLOCALISATION_ET_VALIDATION|Suivant →]]
