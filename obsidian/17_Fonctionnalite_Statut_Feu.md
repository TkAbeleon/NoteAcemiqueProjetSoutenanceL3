# ✅ Fonctionnalité — Statut d’un feu (Actif / En baisse / Probablement éteint)
#JeryMotro #MemoireL3 #Feature #Workflow #Alerte #FIRMS
[[Glossaire_Tags]] | [[00_INDEX]] | [[05_HDBSCAN_Clustering]] | [[12_Systeme_Alertes]] | [[09_FastAPI_Backend]]

> Objectif : déduire un **statut “feu éteint ou non”** à partir des détections **NASA FIRMS (Active Fire)**, qui ne fournissent pas de champ “extinguished”.

---

## 1) Problème (limite FIRMS)

Les CSV FIRMS (MODIS/VIIRS) contiennent des **détections positives** de chaleur active (ex : `acq_date`, `acq_time`, `frp`, `brightness`, etc.), mais :
- il n’existe **pas** de colonne “feu éteint”
- FIRMS ne fournit pas de “non-détection” explicite

Donc : on ne peut pas “confirmer” l’extinction avec FIRMS seul, on peut seulement **l’inférer** via l’absence de détections pendant une durée donnée.

---

## 2) À quoi ça sert dans JeryMotro (valeur produit)

- **Alerte intelligente** : éviter d’envoyer la même alerte tant que le feu n’évolue pas.
- **Dashboard plus crédible** : afficher un état lisible (*Actif*, *En baisse*, *Probablement éteint*).
- **Statistiques** : estimer une durée d’activité par cluster (approximative) pour le suivi hebdo.

---

## 3) Données nécessaires (dans les CSV)

Exemple (VIIRS) : `fire_nrt_SV-C2_704593.csv`
Colonnes utiles :
- localisation : `latitude`, `longitude`
- temps : `acq_date`, `acq_time`
- intensité : `frp`, `brightness`, `bright_t31/ti5`
- qualité : `confidence` (catégorielle en VIIRS, numérique en MODIS), `scan`, `track`

⚠️ Important : le statut ne peut être calculé **que relativement** à une date de référence `now` (souvent = “date/heure de run pipeline”).

---

## 4) Principe : regrouper puis mesurer “dernier signal”

### 4.1 Regroupement recommandé : clusters spatio-temporels
On ne raisonne pas point-par-point, mais par **événement** (cluster).

Référence clustering : [[05_HDBSCAN_Clustering]] (750m / 48h, min_cluster_size=3).

Pour chaque cluster, on calcule au minimum :
- `first_seen` = date/heure de la première détection
- `last_seen` = date/heure de la dernière détection
- `duration_hours` = `last_seen - first_seen`
- (optionnel) `max_frp`, `frp_total`, `cluster_size`

### 4.2 Statut = fonction du temps depuis la dernière détection
On pose :
- `delta = now - last_seen`

Puis on affecte un statut.

---

## 5) Méthode complète : statut + incertitude + réactivation

> Idée clé : avec FIRMS, “éteint” n’est jamais une vérité terrain, c’est un **diagnostic opérationnel** basé sur le dernier signal *et* sur la qualité d’observation (nuages, trous de collecte, capteurs indisponibles).

### 5.1 États (machine d’état)
- `ACTIVE` : détections récentes (feu actif / en cours)
- `COOLING` : plus de détection récente, mais incertitude encore élevée
- `LIKELY_OUT` : plus de détection depuis longtemps → “probablement éteint”
- `UNKNOWN` : impossible de conclure (trou de collecte / observation dégradée)

### 5.2 Seuils (par défaut)
Seuils simples (à ajuster selon tests). Si ton CRON est **toutes les 3 heures**, utiliser les seuils proposés en **6.2.1** :
- `ACTIVE` si `delta <= 6h`
- `COOLING` si `6h < delta <= 24h`
- `LIKELY_OUT` si `delta > 48h`

> Pourquoi une zone “24h–48h” ?
> Parce que l’absence de détection peut venir du contexte (nuages, survol, feu trop faible). On laisse une zone tampon.

### 5.3 Gestion “nuages” (anti faux éteint)
Le CSV FIRMS ne contient pas directement une info “nuage”. Donc on traite ce risque de deux manières :

**A) MVP (sans données nuage)** — règle prudente :
- si la collecte est incomplète récemment (une ou plusieurs sources en échec) → statut `UNKNOWN` (ne jamais conclure `LIKELY_OUT`)
- si le pipeline n’a pas tourné depuis longtemps (ex: `now - last_pipeline_run > 2h`) → statuts considérés obsolètes (*stale*) ou forcés à `UNKNOWN`

**B) Recommandé (avec une variable nuage via GEE/ERA5 ou autre source)** :
- calculer un indicateur `cloud_risk` autour du cluster sur la période `last_seen → now`
- si nuages élevés (ex: `cloud_risk = HIGH`) :
  - ne jamais passer en `LIKELY_OUT` avant `delta > 72h`
  - rester en `COOLING` ou `UNKNOWN`

> Résultat : on réduit le cas “on croit que c’est éteint mais c’était juste caché”.

### 5.4 Réactivation (si le feu revient, il n’était pas éteint)
Règle demandée : si le feu est “supposé éteint” puis revient, on dit qu’il **n’était pas éteint** (extinction supposée fausse).

Quand une nouvelle détection arrive après un `LIKELY_OUT` :
- on repasse immédiatement à `ACTIVE`
- on enregistre un événement `REACTIVATED`
- on garde l’historique pour le dashboard (et pour expliquer les limites FIRMS au jury)

### 5.5 Identifiant persistant : `fire_id` (car `cluster_id` change)
`cluster_id` peut changer entre runs → on crée un identifiant stable `fire_id`.

**Liaison simple entre runs (recommandée)** :
- pour un cluster courant `C` (centre, `first_seen`, `last_seen`)
- chercher un cluster historique `H` tel que :
  - distance(centre_C, centre_H) ≤ 1 km (ou 750m)
  - et `first_seen_C - last_seen_H` ≤ 72h
- si trouvé : `fire_id = fire_id(H)`, sinon créer un nouveau `fire_id`

Cela permet de dire : “ce feu a été actif, puis supposé éteint, puis réactivé”.

### 5.6 Champs à stocker (minimum)
Dans la BDD (table `clusters` enrichie ou table dédiée `fire_events`) :
- `fire_id` (stable)
- `first_seen`, `last_seen`
- `cluster_status` (`ACTIVE|COOLING|LIKELY_OUT|UNKNOWN`)
- `hours_since_last_seen`
- `status_reason` (ex: `RECENT_DETECTION`, `NO_DETECTION_48H`, `DATA_GAP`, `CLOUD_HIGH`, `REACTIVATED`)
- (optionnel) `reactivation_count`, `out_revoked_at`

---

## 6) Règles de collecte automatique (pour savoir si le feu est actif)

> Sans collecte fiable, le statut sera faux. Ces règles “ingénierie” font partie de la soutenance.

### 6.1 Fréquence
- Pipeline/CRON : **toutes les 3 heures** (choix technique).

**Justification (mémoire)** :
- La détection FIRMS dépend des **passages satellites** (MODIS/VIIRS) et la revisite n’est pas continue.
- Un CRON 3h est un compromis raisonnable : moins de charge (API/DB) tout en capturant les nouvelles détections au rythme des survols.

⚠️ Condition pour que ce choix soit correct : appliquer une **fenêtre glissante** (6.2) + déduplication (6.4) afin de ne pas “rater” des détections entre deux runs ou en cas de retard NRT.

### 6.2 Fenêtre glissante (retards NRT + trous)
Au lieu de récupérer “seulement depuis 30 minutes”, récupérer une **fenêtre glissante** et dédupliquer.

Recommandation :
- collecter au moins les **dernières 72h** (si la contrainte `DAY_RANGE` le permet), sinon le maximum possible

Référence limite `DAY_RANGE` : [[REF-001_NASA_FIRMS_API]].

### 6.2.1 Paramètres de statut adaptés à un CRON 3h
Comme on observe toutes les 3h, on évite des seuils trop agressifs.

Recommandation (par défaut) :
- `ACTIVE` si `delta <= 9h` (≈ 3 exécutions)
- `COOLING` si `9h < delta <= 24h`
- `LIKELY_OUT` si `delta > 72h` (prudence : trous/nuages/retards)
- `UNKNOWN` si observation dégradée (6.6)

> Ces valeurs sont cohérentes avec la règle “si le feu revient, l’extinction supposée était fausse” (réactivation).

### 6.3 Multi-capteurs (réduit les faux “éteint”)
Toujours collecter les 3 sources :
- `VIIRS_SNPP_NRT`
- `VIIRS_NOAA21_NRT`
- `MODIS_NRT`

Si une source est en panne, on dégrade la qualité d’observation.

### 6.4 Déduplication obligatoire
Clé de déduplication recommandée :
`(latitude, longitude, acq_date, acq_time, satellite, instrument)`

### 6.5 Qualité minimum (avant clustering / statut)
Appliquer des filtres cohérents :
- VIIRS : garder `confidence ∈ {nominal, high}` (voir [[14_Dataset_FIRMS_VIIRS]])
- MODIS : fixer un seuil de `confidence` (voir [[13_Dataset_FIRMS_MODIS]])
- enlever le bruit : `frp >= 1.0` (ou valeur ajustée)

### 6.6 Gestion des échecs (ne jamais conclure “éteint” si on n’observe pas)
Pour chaque run :
- stocker un `collection_health` (OK/KO par source) + `last_pipeline_run`
- si observation dégradée → `cluster_status = UNKNOWN` (au lieu de `LIKELY_OUT`)

---

## 7) Intégration dans la plateforme

### 7.1 Backend (FastAPI)
Endpoints concernés (design) :
- `GET /clusters` : retourner `cluster_status`, `last_seen`, `fire_id`
- `GET /detections` : optionnellement inclure `cluster_status` via jointure cluster→points
- `GET /alerts` : stocker le statut au moment de l’alerte + raison

Référence : [[09_FastAPI_Backend]].

### 7.2 Alertes (anti-spam + réactivation)
- déclencher alerte si `cluster_status == ACTIVE` et (score/FRP dépasse un seuil) — voir [[12_Systeme_Alertes]]
- ne pas renvoyer tant que le cluster reste `ACTIVE` sans changement notable
- si `REACTIVATED` (retour après `LIKELY_OUT`) : autoriser une alerte “reprise d’activité”

### 7.3 n8n (règles de workflow)
Dans `alert_trigger` :
- filtrer `cluster_status == ACTIVE`
- ET (`risk_score > 0.70` OU `frp > 50` OU `cluster_size >= 10`)
- ET éviter les doublons via `fire_id` (ne pas renvoyer la même alerte si déjà envoyée récemment)

Référence : [[11_Automatisation_n8n]].

---

## 8) Exemple (sur un CSV réel)

Sur `fire_nrt_SV-C2_704593.csv` :
- période couverte : **2025-11-01 10:53 → 2026-01-12 10:08** (d’après `acq_date/acq_time`)

Ce CSV seul ne permet pas de savoir ce qui se passe **après** le 12/01/2026 10:08.
Mais si on pose `now = 2026-01-12 10:08` :
- un point/cluster dont le `last_seen` est bien avant `now - 48h` sera classé `LIKELY_OUT` (si observation OK)
- si observation KO (source en panne / pipeline arrêté), on force `UNKNOWN`

---

## 9) Limites (à écrire clairement dans le mémoire)

- **Pas de preuve** d’extinction : FIRMS active fire = “détection”, pas “état”.
- **Non-détection ambiguë** : nuages, fumée, faible intensité, géométrie, fréquence de survol.
- **Seuils heuristiques** : 6h/24h/48h/72h sont des choix d’ingénierie → à justifier et ajuster.

> Formulation “jury-friendly” :
> “On implémente un statut opérationnel basé sur *time-since-last-detection* et la qualité d’observation, afin d’améliorer l’UX et la gestion d’alertes, tout en explicitant qu’il s’agit d’une inférence et non d’une vérité terrain.”
