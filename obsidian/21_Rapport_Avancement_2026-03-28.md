# 📌 Rapport d’avancement — JeryMotro Platform
#JeryMotro #MemoireL3 #Avancement #Milestone
[[Glossaire_Tags]] | [[00_INDEX]] | [[00_DASHBOARD]]

**Date :** 28/03/2026 (Indian/Antananarivo)

---

## ✅ État global (ce qui est OK / fait)

| Élément | Statut | Preuve / Référence |
|---|---|---|
| API NASA FIRMS | ✅ OK | CSV FIRMS présents (`fire_nrt_*.csv`) + endpoints documentés ([[REF-001_NASA_FIRMS_API]]) |
| Collecte automatique des données | ✅ Implémentée (workflow fourni) | Workflow n8n : `Collecte Donnée FIRMS NASA automatique.json` + doc [[11_Automatisation_n8n]] |
| Ingestion DB (Supabase/Postgres) | ✅ Fonctionnelle (au moins sur une période) | Tables vues : `firms_fire_detections`, `alerts`, `users` |
| UML | ✅ Produit | [[20_UML_JeryMotro_Platform]] (use cases, séquences, activités, classes) |
| Spécification accès (public vs alertes) | ✅ Clarifiée | [[19_Acces_Sans_Inscription_Auth_Alertes]] |
| Statut feu (actif/éteint inféré + réactivation) | ✅ Spécifié | [[17_Fonctionnalite_Statut_Feu]] |
| Améliorations DB + workflow (checklist) | ✅ Documenté | [[18_Ameliorations_DB_Workflow]] |

---

## 🔎 Détails techniques constatés (à date)

### Collecte FIRMS (workflow fourni)
- **Trigger** : toutes les **3 heures**.
- **Sources effectivement appelées** dans le JSON fourni : `MODIS_NRT` + `VIIRS_NOAA20_NRT`.
- **BBOX du workflow** : `43,-26,51,-11` (diffère de la bbox documentée dans `00_INDEX.md`).
- **Fenêtre** : `.../1` sur l’API FIRMS (puis déduplication côté insertion).
- **Traitement** : parse CSV → filtrage (coords, date/heure, `frp > 0`) → normalisation → génération d’un `INSERT ... ON CONFLICT`.

### Base de données (Supabase/Postgres) — état observé
- Tables pertinentes vues : `firms_fire_detections`, `alerts`, `users`, `firms_summary_24h`, `firms_hotspots`.
- Données présentes (indicateur de fonctionnement) :
  - `firms_fire_detections` : **1729** lignes.
  - `alerts` : **7** lignes.
  - dernière détection (`max(acq_datetime)`) : **2026-03-26 12:08 UTC**
  - dernière ingestion (`max(inserted_at)`) : **2026-03-26 14:00 UTC**
- Point important : pas de table `clusters/fire_events` dans le schéma observé → le statut “éteint” n’est pas encore stocké nativement (il est seulement spécifié dans [[17_Fonctionnalite_Statut_Feu]]).

---

## 🟡 Partiellement OK / À consolider

| Élément | Statut | Commentaire |
|---|---|---|
| Collecte (régularité / santé) | 🟡 | Ajouter un log de run (`collection_runs`) + health par source pour éviter les “faux éteint” (voir [[17_Fonctionnalite_Statut_Feu]] + [[18_Ameliorations_DB_Workflow]]) |
| Alertes (mail/WhatsApp/SMS) | 🟡 | Spécifié dans [[12_Systeme_Alertes]] ; à valider avec tests réels et anti-spam |
| “Bot” avec accès DB | 🟡 | Mentionné, mais pas localisé dans ce dossier (merci d’indiquer le chemin/repo) |
| Prototype Symfony (toutes fonctionnalités regroupées) | 🟡 | Non trouvé dans ce dossier (pas de `composer.json` détecté) → à pointer (chemin/repo) |

---

## 📎 Livrables / fichiers présents (dans ce dossier)

- Workflow n8n : `Collecte Donnée FIRMS NASA automatique.json`
- Échantillons CSV FIRMS : `fire_nrt_M-C61_704589.csv`, `fire_nrt_M-C61_704592.csv`, `fire_nrt_SV-C2_704593.csv`
- Docs : `16_Role_ML_DL_JeryMotroNet.md`, `17_Fonctionnalite_Statut_Feu.md`, `18_Ameliorations_DB_Workflow.md`, `19_Acces_Sans_Inscription_Auth_Alertes.md`, `20_UML_JeryMotro_Platform.md`

---

## ⚠️ Points à corriger en priorité (observés sur le workflow JSON)

- La MAP_KEY FIRMS est présente en clair dans `Collecte Donnée FIRMS NASA automatique.json` → à basculer vers `{{$env.FIRMS_MAP_KEY}}` / credentials.
- Les nœuds HTTP/DB ne semblent pas configurés pour “continue on fail” + retries → risque d’arrêt complet sur un timeout.
- Le nœud SQL “Générer SQL INSERT” contient une fin de script suspecte (`};fa`) → à vérifier/corriger (sinon exécutions KO).
- Sources VIIRS à aligner avec la doc (SNPP + NOAA21) + bbox à aligner avec `00_INDEX.md`.

---

## 🎯 Prochaines actions (recommandées)

1. Corriger/fiabiliser le workflow : secrets (MAP_KEY), retries, multi-capteurs, bbox unique, logs de run (voir [[18_Ameliorations_DB_Workflow]]).
2. Ajouter en DB : `collection_runs` + (optionnel) `fire_events`/`clusters` (`fire_id`, `last_seen`, `cluster_status`) pour supporter [[17_Fonctionnalite_Statut_Feu]].
3. Valider alertes : test mail + WhatsApp + SMS, puis ajouter anti-spam (dédup par `fire_id` + cooldown).
4. Me donner le chemin du prototype Symfony + du bot DB pour que je puisse les auditer et les relier à la doc/UML.
