# Règles de gestion — JeryMotro

## Objet

Ce document formalise les règles métier déduites du backend réel de JeryMotro. Il sert de référence entre le code, le dictionnaire de données et le diagramme de classes.

## Utilisateurs

### RG01 — Identification unique
Chaque utilisateur possède une adresse e-mail obligatoire et unique.

### RG02 — Rôle
Chaque utilisateur possède un rôle parmi `standard`, `premium` et `admin`. Le rôle par défaut est `standard`.

### RG03 — État du compte
Un utilisateur possède un état `is_active` indiquant si le compte est actif.

## Abonnements d'alerte

### RG04 — Appartenance
Chaque abonnement d'alerte appartient à un utilisateur.

### RG05 — Un abonnement par canal
Pour un utilisateur donné, un seul abonnement existe pour un canal donné. La combinaison `(user_id, channel)` est unique.

### RG06 — Canaux autorisés
Les canaux d'alerte sont `EMAIL`, `SMS` et `WHATSAPP`.

### RG07 — Accès SMS/WhatsApp
Les canaux SMS et WhatsApp sont réservés aux utilisateurs `premium` et `admin`.

### RG08 — Vérification avant envoi
Un abonnement doit être à la fois activé (`enabled`) et vérifié (`is_verified`) pour être éligible à l'envoi automatique.

### RG09 — Nouvelle vérification après changement de destination
La modification de la destination d'un abonnement rend l'abonnement non vérifié et provoque une nouvelle demande de vérification.

### RG10 — Code de vérification temporaire
Le code de vérification d'un abonnement est constitué de 6 chiffres et possède une date d'expiration. Un nouveau code réinitialise la procédure de vérification.

### RG11 — Limite de tentatives
La vérification d'un abonnement est limitée à 3 tentatives incorrectes. Après dépassement, un nouveau code doit être demandé.

### RG12 — Seuils propres à l'abonnement
Chaque abonnement possède un seuil minimal de risque `min_risk` et un seuil minimal de FRP `min_frp`.

## Zones surveillées

### RG13 — Appartenance
Chaque zone surveillée appartient obligatoirement à un utilisateur.

### RG14 — Définition géographique
Une zone est définie par un nom, un centre (latitude, longitude) et un rayon en kilomètres. Le rayon par défaut est de 10 km.

### RG15 — Paramètres de zone
Une zone peut définir ses propres seuils `min_risk` et `min_frp`, ainsi qu'un `custom_ai_prompt`.

## Détections FIRMS

### RG16 — Position et acquisition
Chaque détection possède obligatoirement une latitude, une longitude et une date d'acquisition.

### RG17 — Unicité d'une détection
La combinaison `latitude + longitude + acq_date + acq_time + satellite + instrument` est unique afin d'éviter les doublons.

### RG18 — Association facultative à un événement
Une détection peut être affectée à un `FireEvent` par `fire_event_id`. Cette association est facultative dans le modèle.

### RG19 — Résultats de traitement
Une détection peut conserver les résultats du traitement : score de risque, label, cluster, indicateurs de cluster, bruit et région.

## Événements de feu et regroupement

### RG20 — Identifiant stable
Chaque événement de feu possède un `fire_id` unique et stable.

### RG21 — Construction d'un événement
Un événement de feu est construit à partir d'un groupe de détections.

### RG22 — Regroupement
Le système utilise HDBSCAN lorsque disponible et dispose d'un regroupement par grille en solution de secours.

### RG23 — Bruit
Les détections identifiées comme bruit (`-1` dans le clustering) ne constituent pas un événement de feu.

### RG24 — Agrégation
Un événement synthétise notamment le centroïde, le nombre de détections, les FRP total et maximal, le risque maximal, les dates de première et dernière observation, la durée et la région.

## Risque

### RG25 — Normalisation
Le score de risque valide est normalisé entre `0.0` et `1.0`. Une valeur absente ou négative représente un score indisponible.

### RG26 — Niveau de risque
Le niveau est déterminé par les règles suivantes :

| Condition | Niveau |
|---|---|
| `frp > 50` | `CRITICAL` |
| `risk_score >= 0.80` | `CRITICAL` |
| `risk_score >= 0.60` | `HIGH` |
| `risk_score >= 0.40` | `MEDIUM` |
| `risk_score < 0.40` | `LOW` |
| score absent/négatif et `frp <= 50` | `UNKNOWN` |

Le seuil FRP `> 50` est prioritaire.

## Statut des feux

### RG27 — Valeurs de statut
Un événement possède un statut parmi `ACTIVE`, `COOLING`, `LIKELY_OUT` et `UNKNOWN`.

### RG28 — Défaillance de collecte
Si le pipeline n'est pas sain, le statut est `UNKNOWN` avec la raison `DATA_GAP`.

### RG29 — Feu actif
Si la dernière détection date de 9 heures ou moins, le statut est `ACTIVE`.

### RG30 — Feu en refroidissement
Au-delà de 9 heures et jusqu'à 72 heures sans nouvelle détection, le statut est `COOLING`. La raison distingue les seuils 9 h et 24 h.

### RG31 — Feu probablement éteint
Au-delà de 72 heures sans nouvelle détection, le statut devient `LIKELY_OUT`.

### RG32 — Réactivation
Un événement `LIKELY_OUT` peut être réactivé lorsqu'une nouvelle détection est observée. Le modèle conserve `reactivation_count`.

## Alertes générées

### RG33 — Contexte d'une alerte
Une alerte peut référencer l'utilisateur destinataire, un événement de feu et une détection.

### RG34 — Canal et destination
Une alerte conserve le canal et la destination effectivement utilisés.

### RG35 — État de l'envoi
Le statut d'envoi est conservé parmi `PENDING`, `SENT` et `FAILED`. Une erreur peut être conservée.

### RG36 — Éligibilité d'une alerte automatique
Une alerte automatique cible les abonnements activés, vérifiés et autorisés pour leur canal, lorsque `risk_score >= min_risk` OU `frp >= min_frp`.

## Collectes

### RG37 — Traçabilité
Chaque exécution de collecte possède un `run_id` unique et est enregistrée dans `CollectionRun`.

### RG38 — Résultat de collecte
Une collecte conserve sa source, ses dates, son état, les volumes brut/valides/dédoublonnés et une éventuelle erreur.

### RG39 — Collecte automatique
La collecte automatique est périodique et alimente ensuite le pipeline de traitement des détections.

## Prédictions

### RG40 — Données minimales
Une prédiction possède obligatoirement une date, une position et un score de risque J+1.

### RG41 — Contexte de prédiction
Une prédiction peut conserver une maille, une confiance, une version de modèle, une fenêtre historique et une région.

### RG42 — Pas de relation inventée
Le modèle `Prediction` actuel ne possède pas de clé étrangère vers `User`, `FireEvent` ou `FirmsFireDetection`. Ces relations ne doivent donc pas être ajoutées sans preuve dans le diagramme de classes.

## Règles pour la modélisation UML

### RG43 — Cardinalités
Les cardinalités doivent être fondées sur les contraintes et associations réellement présentes dans le modèle de données et dans les règles métier.

### RG44 — Énumérations
Les énumérations métier identifiées sont `UserRole`, `AlertChannel` et `FireStatus`.

### RG45 — Attributs calculés
Les valeurs telles que `risk_level`, `cluster_frp_total`, `cluster_frp_max`, `duration_hours` et `hours_since_last_seen` doivent être distinguées des données élémentaires lorsqu'elles sont calculées par le système.

## Points à vérifier

- `FirmsFireDetection.collection_run_id` et `CollectionRun.run_id` existent tous les deux, mais `collection_run_id` n'est pas déclaré comme `ForeignKey` dans le modèle de détection.
- `Prediction` n'expose pas de clé étrangère vers les autres entités principales.
- Les opérations UML doivent rester limitées aux comportements métier réellement utiles ; une grande partie de la logique est portée par les services et routeurs.
- NASA FIRMS, le service ML, n8n, Qdrant et les fournisseurs de notification sont des composants externes : leurs interactions seront représentées dans les diagrammes d'activité, de séquence, de composants ou d'architecture plutôt que comme associations de persistance.

## Références principales du backend

- `Backend/api/models/user.py`
- `Backend/api/models/alert_subscription.py`
- `Backend/api/models/alert.py`
- `Backend/api/models/zone.py`
- `Backend/api/models/detection.py`
- `Backend/api/models/cluster.py`
- `Backend/api/models/prediction.py`
- `Backend/api/models/collection_run.py`
- `Backend/api/services/jerymotronet_service.py`
- `Backend/api/services/cluster_service.py`
- `Backend/api/services/fire_status_service.py`
- `Backend/api/routers/alerts.py`
