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

PostgreSQL est **installé localement sur la VM GCP Debian 13** et constitue la base relationnelle de production du backend.

```text
GCP / Debian 13
     |
     +-- PostgreSQL (local)
     +-- FastAPI / Uvicorn
     +-- Nginx
     +-- n8n
     +-- Qdrant
     +-- WAHA
```

Le backend y accède par SQLAlchemy + `asyncpg`, avec une URL de connexion fournie par `DATABASE_URL`.

La configuration Nginx ne publie pas PostgreSQL sur un sous-domaine HTTP : le port SQL reste distinct du trafic Web. Les valeurs exactes d'hôte, utilisateur, mot de passe et base ne sont pas reproduites dans la documentation.

---

**Navigation :** [[04_PIPELINE_DONNEES|← Précédent]] | [[00_INDEX|Index]] | [[06_GEOLOCALISATION_ET_VALIDATION|Suivant →]]
