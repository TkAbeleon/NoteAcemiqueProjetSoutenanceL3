# 🛠️ Améliorations — Base de données & Workflow de collecte (n8n)
#JeryMotro #MemoireL3 #DevOps #Workflow #Database #Solution
[[Glossaire_Tags]] | [[00_INDEX]] | [[08_Docker_Infrastructure]] | [[11_Automatisation_n8n]] | [[17_Fonctionnalite_Statut_Feu]]

> Ce document liste les améliorations concrètes à faire côté **workflow n8n** et **PostgreSQL/Supabase** pour fiabiliser :
> 1) la collecte automatique FIRMS, 2) l’historisation, 3) le statut “feu actif/éteint (inféré)”.

---

## 1) Workflow n8n (Collecte FIRMS)

Fichier analysé : `Collecte Donnée FIRMS NASA automatique.json`.

### 1.1 Correctifs immédiats (à faire en premier)
- **Corriger le code JS** du nœud `📝 Générer SQL INSERT` (fin de script invalide : caractères parasites).
- Activer la tolérance aux pannes :
  - `🛰 HTTP …` : activer “continue on fail” + retries/backoff.
  - `🐘 PostgreSQL …` : gérer explicitement la branche “error” (et n’envoyer `❌ Log Erreur DB` que sur erreur).
- **Retirer la MAP_KEY du JSON** :
  - utiliser `{{$env.FIRMS_MAP_KEY}}` (ou un credential n8n), jamais une valeur en clair.

### 1.2 Qualité de collecte (pour réduire les faux “éteint”)
- **Fenêtre glissante** + déduplication (obligatoire) :
  - ex : récupérer plusieurs jours, puis dédupliquer avant insertion.
- **Multi-capteurs** :
  - ajouter `VIIRS_SNPP_NRT` et `VIIRS_NOAA21_NRT` (en plus de MODIS) pour améliorer l’observabilité.
- **BBOX unique** :
  - harmoniser la bbox avec le cahier des charges (évite incohérences dataset/BDD).
- **Filtres cohérents** :
  - VIIRS : exclure `low` ; MODIS : seuil de `confidence` ; `frp >= 1.0` si tu veux limiter le bruit.

### 1.3 Observabilité (pour le mémoire + debug)
- Ajouter un enregistrement de run (voir table `collection_runs`) :
  - date run, sources OK/KO, nb lignes brutes, nb valides, nb dédupliquées, erreur (si KO).
- Ajouter un “heartbeat” (keepalive) alimenté à chaque run OK.

---

## 2) Base PostgreSQL/Supabase

### 2.1 Contraintes & déduplication (ingestion robuste)
- Éviter une contrainte UNIQUE sur des `double precision` bruts si possible.
  - Option simple : stocker `latitude/longitude` en `numeric(8,5)` (ou arrondir avant insert).
- Garder une contrainte UNIQUE stable (exemple) :
  - `(source, latitude, longitude, acq_datetime, satellite)`

### 2.2 Index indispensables
- Index temps : `acq_datetime`
- (Si statut feu) index pour “last seen” :
  - `(latitude, longitude, acq_datetime)` ou un index spatial si tu ajoutes PostGIS
- Si PostGIS est utilisé : ajouter une colonne `geog geography(Point,4326)` + index GIST.

### 2.3 Tables recommandées pour le statut feu
Pour implémenter la logique de [[17_Fonctionnalite_Statut_Feu]] correctement :
- `collection_runs` :
  - `run_id`, `started_at`, `finished_at`, `source`, `ok`, `row_count_raw`, `row_count_valid`, `row_count_dedup`, `error`
- `fire_events` (ou `clusters`) :
  - `fire_id`, `first_seen`, `last_seen`, `cluster_status`, `status_reason`, `reactivation_count`
- `fire_event_history` (optionnel, très utile mémoire) :
  - `fire_id`, `changed_at`, `old_status`, `new_status`, `reason`

### 2.4 Vues utiles (pour API / dashboard)
- `firms_last_seen_by_cell` (ou par cluster) : dernière détection par zone.
- `firms_summary_24h` : OK si alimentée, mais ajouter aussi :
  - “last run ok”, “sources ok/ko”, etc.

---

## 3) Check “est-ce que c’est fiable ?” (règles simples)

Tu peux considérer un statut “LIKELY_OUT” comme valide uniquement si :
- la collecte est **saine** (runs OK récents, sources OK),
- et tu as observé au moins `T_out` après la dernière détection (`last_seen`),
- sinon : `UNKNOWN`.

Ces règles rendent la conclusion défendable au jury.

