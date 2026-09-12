# Dictionnaire de données — JeryMotro

Ce dictionnaire décrit les principales entités persistées du backend réel de JeryMotro. Il sert de référence pour le diagramme de classes et les autres diagrammes UML.

> **Source de vérité :** modèles SQLAlchemy et logique métier actuellement présents dans `JeryMotroBackend/Backend/api/`.

## 1. User

| Champ | Type | Contraintes / rôle |
|---|---|---|
| `id` | Integer | Clé primaire |
| `email` | String | Obligatoire, unique |
| `hashed_password` | String | Mot de passe haché |
| `full_name` | String | Nom complet |
| `organization` | String | Organisation |
| `role` | UserRole | `standard`, `premium`, `admin` |
| `phone_number` | String | Numéro SMS |
| `whatsapp_number` | String | Numéro WhatsApp |
| `phone_verified` | Boolean | Vérification du téléphone |
| `otp_code_hash` | String | Donnée temporaire d'authentification OTP |
| `otp_expires_at` | DateTime | Expiration OTP |
| `otp_attempts` | Integer | Tentatives OTP |
| `is_active` | Boolean | État du compte |
| `created_at` | DateTime | Création |
| `updated_at` | DateTime | Dernière modification |

## 2. AlertSubscription

| Champ | Type | Contraintes / rôle |
|---|---|---|
| `id` | BigInteger | Clé primaire |
| `user_id` | BigInteger | FK vers `User.id` |
| `channel` | AlertChannel | `EMAIL`, `SMS`, `WHATSAPP` |
| `destination` | String | Adresse ou numéro destinataire |
| `enabled` | Boolean | Abonnement actif ou non |
| `min_risk` | Float | Seuil minimal de risque |
| `min_frp` | Float | Seuil minimal de FRP |
| `is_verified` | Boolean | Destination vérifiée |
| `verification_code` | String | Code de vérification |
| `verification_expires_at` | DateTime | Expiration du code |
| `verification_attempts` | Integer | Tentatives de vérification |
| `created_at` | DateTime | Création |
| `updated_at` | DateTime | Dernière modification |

**Contrainte :** unicité de `(user_id, channel)`.

## 3. MonitoredZone

| Champ | Type | Contraintes / rôle |
|---|---|---|
| `id` | Integer | Clé primaire |
| `user_id` | Integer | FK vers `User.id` |
| `name` | String | Nom de la zone |
| `latitude` | Float | Centre de la zone |
| `longitude` | Float | Centre de la zone |
| `radius_km` | Float | Rayon en km, défaut 10 km |
| `min_risk` | Float | Seuil de risque de la zone |
| `min_frp` | Float | Seuil FRP de la zone |
| `custom_ai_prompt` | Text | Contexte IA personnalisé |
| `created_at` | DateTime | Création |
| `updated_at` | DateTime | Dernière modification |

## 4. FirmsFireDetection

| Champ | Type | Rôle |
|---|---|---|
| `id` | BigInteger | Clé primaire |
| `source` | String | Source FIRMS |
| `satellite` | String | Satellite |
| `instrument` | String | Instrument |
| `latitude` | Float | Latitude |
| `longitude` | Float | Longitude |
| `acq_date` | Date | Date d'acquisition |
| `acq_time` | String | Heure d'acquisition |
| `acq_datetime` | DateTime | Date/heure complète |
| `local_hour` | Integer | Heure locale |
| `brightness` | Float | Luminosité |
| `bright_t31` | Float | Température de brillance bande 31 |
| `diff_brightness` | Float | Différence de luminosité |
| `frp` | Float | Fire Radiative Power |
| `frp_log` | Float | FRP transformé |
| `confidence` | String | Confiance FIRMS |
| `confidence_num` | Integer | Confiance numérique |
| `daynight` | String | Jour/nuit |
| `scan` | Float | Balayage |
| `track` | Float | Suivi |
| `scan_track_ratio` | Float | Ratio scan/track |
| `is_dry_season` | Boolean | Saison sèche |
| `temperature_2m` | Float | Température à 2 m |
| `relative_humidity` | Float | Humidité relative |
| `wind_speed` | Float | Vitesse du vent |
| `precipitation` | Float | Précipitation |
| `landcover` | String | Couverture terrestre |
| `slope_deg` | Float | Pente |
| `ndvi_10m` | Float | NDVI |
| `is_recent_loss` | Integer | Perte récente |
| `risk_score` | Float | Score de risque calculé |
| `fire_label` | Integer | Résultat du modèle |
| `cluster_id` | Integer | Identifiant de cluster |
| `fire_event_id` | BigInteger | FK optionnelle vers `FireEvent.id` |
| `cluster_size` | Integer | Taille du cluster |
| `cluster_frp_total` | Float | FRP total du cluster |
| `cluster_frp_max` | Float | FRP maximal du cluster |
| `is_noise` | Integer | Indique un point bruit |
| `region` | String | Région géographique |
| `collection_run_id` | String | Identifiant de collecte |
| `inserted_at` | DateTime | Insertion |
| `updated_at` | DateTime | Dernière modification |

**Contrainte métier :** unicité de `latitude + longitude + acq_date + acq_time + satellite + instrument`.

## 5. FireEvent

| Champ | Type | Rôle |
|---|---|---|
| `id` | BigInteger | Clé primaire |
| `fire_id` | String | Identifiant stable et unique |
| `center_latitude` | Float | Latitude du centroïde |
| `center_longitude` | Float | Longitude du centroïde |
| `radius_km` | Float | Rayon estimé |
| `region` | String | Région |
| `cluster_size` | Integer | Nombre de détections |
| `cluster_frp_total` | Float | FRP total |
| `cluster_frp_max` | Float | FRP maximal |
| `risk_score_max` | Float | Risque maximal |
| `risk_level` | String | Niveau de risque dérivé |
| `first_seen` | DateTime | Première observation |
| `last_seen` | DateTime | Dernière observation |
| `duration_hours` | Float | Durée estimée |
| `hours_since_last_seen` | Float | Temps depuis dernière observation |
| `cluster_status` | FireStatus | Statut métier |
| `status_reason` | String | Justification du statut |
| `reactivation_count` | Integer | Nombre de réactivations |
| `created_at` | DateTime | Création |
| `updated_at` | DateTime | Dernière modification |

## 6. Alert

| Champ | Type | Rôle |
|---|---|---|
| `id` | BigInteger | Clé primaire |
| `user_id` | BigInteger | FK nullable vers `User.id` |
| `fire_event_id` | BigInteger | FK nullable vers `FireEvent.id` |
| `detection_id` | BigInteger | FK nullable vers `FirmsFireDetection.id` |
| `alert_level` | String | Niveau d'alerte |
| `region` | String | Région |
| `latitude` | Float | Latitude |
| `longitude` | Float | Longitude |
| `risk_score` | Float | Score de risque |
| `frp` | Float | Fire Radiative Power |
| `message` | Text | Message envoyé |
| `images` | Array[String] | Images éventuelles |
| `channel` | String | Canal utilisé |
| `destination` | String | Destination |
| `status` | String | `PENDING`, `SENT`, `FAILED` |
| `error_message` | Text | Erreur éventuelle |
| `sent_at` | DateTime | Date d'envoi |
| `created_at` | DateTime | Création |

## 7. Prediction

| Champ | Type | Rôle |
|---|---|---|
| `id` | BigInteger | Clé primaire |
| `prediction_date` | Date | Date de prédiction |
| `latitude` | Float | Latitude de la maille |
| `longitude` | Float | Longitude de la maille |
| `grid_cell_id` | String | Identifiant de maille |
| `risk_score_j1` | Float | Risque prévu à J+1 |
| `confidence` | Float | Confiance |
| `model_version` | String | Version du modèle |
| `input_window_days` | Integer | Fenêtre historique |
| `region` | String | Région |
| `created_at` | DateTime | Création |

**Attention :** aucune FK vers `User`, `FireEvent` ou `FirmsFireDetection` n'est actuellement exposée par le modèle.

## 8. CollectionRun

| Champ | Type | Rôle |
|---|---|---|
| `id` | BigInteger | Clé primaire |
| `run_id` | String | Identifiant unique de l'exécution |
| `source` | String | Source de collecte |
| `started_at` | DateTime | Début |
| `finished_at` | DateTime | Fin |
| `ok` | Boolean | Réussite |
| `row_count_raw` | Integer | Lignes brutes |
| `row_count_valid` | Integer | Lignes valides |
| `row_count_dedup` | Integer | Lignes après déduplication |
| `error` | Text | Erreur éventuelle |
| `created_at` | DateTime | Création |

**Attention :** `FirmsFireDetection.collection_run_id` est un `String` et n'est pas une FK déclarée vers `CollectionRun`.

## 9. Énumérations métier

### UserRole
`standard`, `premium`, `admin`

### AlertChannel
`EMAIL`, `SMS`, `WHATSAPP`

### FireStatus
`ACTIVE`, `COOLING`, `LIKELY_OUT`, `UNKNOWN`

## 10. Associations à représenter

- `User 1 — 0..* AlertSubscription`
- `User 1 — 0..* MonitoredZone`
- `User 1 — 0..* Alert`
- `FireEvent 1 — 0..* FirmsFireDetection` avec FK optionnelle côté détection
- `FireEvent 1 — 0..* Alert`
- `AlertSubscription → AlertChannel`
- `FireEvent → FireStatus`
- `User → UserRole`

**Relation CollectionRun :** le champ `collection_run_id` existe dans la détection mais n'est pas une FK déclarée ; elle est donc documentée comme lien technique à vérifier plutôt que comme association forte du modèle persistant.

## 11. Origine des données

Les données et contraintes sont alignées sur `Backend/UML/data_dictionary.md`, les modèles SQLAlchemy et `Backend/UML/Regles_de_gestion.md` du backend JeryMotro.
