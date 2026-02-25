# 📋 Cahier des Charges — JeryMotro Platform v2.2
#JeryMotro #MemoireL3 #Soutenance
[[Glossaire_Tags]] | [[00_INDEX]]

> **Référence absolue du projet. Tout autre document s'y réfère.**
> Version 2.2 — mise à jour 23/02/2026 (ajout Docker + FastAPI + Frontend)

---

## IDENTIFICATION DU PROJET

| Champ          | Valeur                                            |
| -------------- | ------------------------------------------------- |
| **Nom**        | JeryMotro Platform                                  |
| **Version**    | 2.2                                               |
| **Niveau**     | Mémoire L3 Génie Logiciel                         |
| **Spécialité** | Développement IA/ML + Backend + Frontend + DevOps |
| **Encadrante** | RANDRIAMIARISON Zilga Heritiana                   |
| **Durée**      | 3 mois (23/02/2026 → 23/05/2026)                  |
| **Nature**     | Projet académique — prototype fonctionnel         |
| **Budget**     | 0 Ar (ressources entièrement gratuites)           |

---

## 1. CONTEXTE & PROBLÉMATIQUE

### 1.1 Les données disponibles

Les données FIRMS NASA (MODIS + VIIRS) fournissent des **points de détection de feux actifs** avec les colonnes :

```
latitude, longitude, brightness, scan, track, acq_date, acq_time,
satellite, instrument, confidence, version, bright_t31, frp, daynight
```

### 1.2 Limites identifiées

| Limite | Impact |
|--------|--------|
| Décalage NRT de 0,5 à 6h | Alertes tardives → voir [[PROB-001_Retard_NRT]] |
| Sous-estimation petits feux < 1ha (tavy/savane) | Détection incomplète → voir [[PROB-002_Petits_feux_tavy]] |
| Données brutes non exploitables localement | Aucun outil local de décision |

### 1.3 Problématique centrale

> *Comment développer, en 3 mois, une plateforme logicielle complète (collecte → ML/DL → API → Frontend → Alertes) qui améliore la détection des feux de brousse à Madagascar en exploitant uniquement les données points FIRMS ?*

### 1.4 Contribution originale

Créer **JeryMotroNet** — un modèle ML/DL original entraîné exclusivement sur données malgaches, et l'intégrer dans une architecture logicielle moderne (Docker + FastAPI + Frontend React/Flutter).

---

## 2. OBJECTIFS

### 2.1 Objectif général

Développer un prototype logiciel complet et déployable qui améliore la détection des feux de brousse à Madagascar via un pipeline automatisé, un modèle IA original et une interface utilisateur claire.

### 2.2 Objectifs spécifiques (mesurables)

| # | Objectif | Indicateur de succès |
|---|----------|---------------------|
| OS1 | Collecte FIRMS automatisée toutes les 30 min via n8n | Données fraîches dans la BDD, zéro intervention manuelle |
| OS2 | Clustering spatio-temporel HDBSCAN des points feu | Clusters cohérents, rayon 750m, fenêtre 48h |
| OS3 | JeryMotroNet : XGBoost + ConvLSTM original | Recall petits feux ≥ +25% vs NASA brut |
| OS4 | Backend FastAPI REST documenté | Swagger UI fonctionnel, endpoints testés |
| OS5 | Frontend React ou Flutter fonctionnel | Carte interactive + chat IA + filtres |
| OS6 | IA explicative RAG (Groq + ChromaDB) | Réponses limitées aux données du projet |
| OS7 | Alertes multi-canal (email + WhatsApp Twilio) | Alerte < 30 min après publication FIRMS |
| OS8 | Infrastructure Docker complète | `docker-compose up` lance toute la stack |

---

## 3. PÉRIMÈTRE TECHNIQUE

### 3.1 In Scope (obligatoire)

- **Données** : Points CSV FIRMS uniquement (MODIS_NRT + VIIRS_SNPP_NRT + VIIRS_NOAA21_NRT)
- **Zone** : Bbox Madagascar `-25.5,43,-11.5,50`
- **Période** : Archives 2020–2025 + NRT quotidien
- **Modèle original** : JeryMotroNet (features FIRMS + ERA5 via GEE)
- **Infrastructure** : Docker + FastAPI + React/Flutter + n8n + ChromaDB

### 3.2 Out of Scope (explicitement exclus)

- ❌ Images satellites brutes Sentinel-2 (optionnel mois 3 uniquement)
- ❌ Application mobile native (Flutter = optionnel selon décision S2)
- ❌ Authentification multi-utilisateurs
- ❌ Déploiement cloud payant
- ❌ Think Tank / Business Canvas / création d'entreprise
- ❌ Burned Area / cartographie post-feu

### 3.3 Optionnel (mois 3, si temps disponible)

- Images GEE → patches 128×128 → U-Net simple
- Export PDF des rapports quotidiens
- Internationalisation (malgache + français)

---

## 4. EXIGENCES FONCTIONNELLES (MoSCoW)

### Must Have — 100% obligatoire pour la soutenance

| # | Exigence | Composant |
|---|----------|-----------|
| M1 | Collecte FIRMS toutes les 30 min via n8n | n8n + Python |
| M2 | Nettoyage + feature engineering (diff_brightness, frp_log, heure locale, saison) | Python |
| M3 | Clustering HDBSCAN (rayon 750m, fenêtre 48h, min_cluster=3) | Python + HDBSCAN |
| M4 | JeryMotroNet XGBoost — classification risque feu/pas feu | ML |
| M5 | JeryMotroNet ConvLSTM — prédiction risque J+1 sur grille 375m | DL |
| M6 | FastAPI — endpoints REST : `/detections`, `/predictions`, `/clusters`, `/alerts`, `/chat` | FastAPI |
| M7 | Frontend (React ou Flutter) — carte interactive + historique + filtres | Frontend |
| M8 | JeryMotro AI — chat Groq-4 + RAG ChromaDB (réponses limitées aux données projet) | IA |
| M9 | Alertes email + WhatsApp Twilio Sandbox (FRP > 50MW ou risque > 0.7) | Alertes |
| M10 | Infrastructure Docker (`docker-compose up` lance tout) | DevOps |

### Should Have — Fortement recommandé

| # | Exigence |
|---|----------|
| S1 | Random Forest régression — prédiction durée/intensité cluster |
| S2 | Export PDF rapport quotidien automatique |
| S3 | Comparaison visuelle MODIS vs VIIRS dans le dashboard |
| S4 | Swagger UI complet pour la FastAPI |

### Could Have — Si temps disponible (mois 3)

| # | Exigence |
|---|----------|
| C1 | Images satellites GEE → U-Net patches 128×128 |
| C2 | Carte de risque hebdomadaire animée |
| C3 | Internationalisation (malgache) |

---

## 5. EXIGENCES NON-FONCTIONNELLES

| Catégorie | Exigence | Seuil |
|-----------|----------|-------|
| Performance | Latence pipeline collecte → prédiction | < 5 min |
| Performance | Latence alerte après publication FIRMS | < 30 min |
| Qualité | Recall petits feux JeryMotroNet vs NASA brut | +25% minimum |
| Code | Couverture tests unitaires FastAPI | ≥ 60% |
| Déploiement | `docker-compose up` fonctionnel | Oui |
| Documentation | README + Swagger + Obsidian vault | Complet |
| Accessibilité | Interface 100% en français | Oui |
| Coût | Budget total | 0 Ar |

---

## 6. ARCHITECTURE LOGICIELLE

Voir détail complet → [[02_Architecture_Globale]]

```
FIRMS API (n8n CRON 30 min)
    ↓
Python Preprocessing (pandas + geopandas)
    ↓ diff_brightness, frp_log, local_hour, is_dry_season, ERA5
HDBSCAN Clustering (750m / 48h)
    ↓
JeryMotroNet
├── XGBoost → risque (0/1) + score
└── ConvLSTM → carte risque J+1 (grille 375m)
    ↓
SQLite + ChromaDB (RAG embeddings)
    ↓
FastAPI (REST Backend)
├── /detections    ← données brutes filtrées
├── /predictions   ← sorties JeryMotroNet
├── /clusters      ← résultats HDBSCAN
├── /alerts        ← historique alertes
└── /chat          ← proxy vers Groq + RAG
    ↓
Frontend (React ou Flutter — décision S2)
├── Carte interactive (Mapbox / Leaflet)
├── Dashboard graphiques saisonniers
├── Chat JeryMotro AI
└── Panneau alertes
    ↓
IF risque > 0.7 OU FRP > 50 MW
└── Twilio WhatsApp + Email
```

---

## 7. STACK TECHNOLOGIQUE COMPLÈTE

| Couche | Technologie | Bibliothèques / Outils | Statut |
|--------|-------------|----------------------|--------|
| **Collecte** | n8n + Python | requests, pandas | Must |
| **Traitement SIG** | Python + QGIS | geopandas, shapely, rasterio | Must |
| **Clustering** | Python | hdbscan, scikit-learn | Must |
| **ML** | Python | xgboost, scikit-learn | Must |
| **DL** | Python + PyTorch | torch, ConvLSTM custom | Must |
| **Backend API** | FastAPI | uvicorn, pydantic, sqlalchemy | Must |
| **Frontend** | React ou Flutter | Leaflet/Mapbox, Recharts (React) OU flutter_map (Flutter) | Must |
| **IA Générative** | Groq API | groq, chromadb, sentence-transformers | Must |
| **Alertes** | Twilio + SMTP | twilio, smtplib | Must |
| **Automatisation** | n8n | HTTP, Python Code, IF, Twilio nodes | Must |
| **Infrastructure** | Docker | docker-compose, Dockerfile par service | Must |
| **BDD** | SQLite → PostgreSQL | sqlalchemy, alembic | Must |
| **Dev** | VS Code + Colab | GitHub, Obsidian | Must |

### 7.1 Décision Frontend — React vs Flutter

> ⚠️ **Décision à prendre avant la fin de S2.**

| Critère | React | Flutter |
|---------|-------|---------|
| Maturité cartes web | ✅ Leaflet, Mapbox matures | 🟡 flutter_map (OK mais moins riche) |
| Performance mobile futur | 🟡 Responsive mais pas natif | ✅ Natif iOS + Android |
| Apprentissage | 🟡 JS/TS à maîtriser | 🟡 Dart à maîtriser |
| Dashboard données | ✅ Recharts / Chart.js | 🟡 fl_chart (suffisant) |
| Déploiement web | ✅ Vercel / Netlify gratuit | 🟡 Flutter Web (acceptable) |
| **Recommandation** | ✅ **React prioritaire** si focus web | Flutter si mobile prévu post-L3 |

→ Documenter la décision dans [[10_Frontend_Decision]]

### 7.2 Docker Services

| Service | Image | Port | Rôle |
|---------|-------|------|------|
| `madfire-api` | python:3.11-slim | 8000 | FastAPI backend |
| `madfire-frontend` | node:20-alpine | 3000 | React (ou flutter web) |
| `madfire-n8n` | n8nio/n8n | 5678 | Automatisation |
| `madfire-chromadb` | chromadb/chroma | 8001 | Vecteurs RAG |
| `madfire-db` | postgres:15 | 5432 | BDD principale |

---

## 8. PLANNING — 3 MOIS (12 SEMAINES)

Voir détail complet → [[03_Plan_Travail_3_Mois]]

| Mois | Semaines | Focus |
|------|----------|-------|
| **Mois 1** | S1–S4 | Infrastructure Docker + Collecte + EDA + Clustering |
| **Mois 2** | S5–S8 | JeryMotroNet + FastAPI + Frontend |
| **Mois 3** | S9–S12 | IA RAG + Alertes + Tests + Mémoire |

**Jalon hebdomadaire :** 1 commit GitHub + Daily Note Obsidian + test pipeline.

---

## 9. RISQUES & MITIGATIONS

| Risque | Probabilité | Impact | Mitigation |
|--------|-------------|--------|------------|
| Décalage NRT FIRMS | Haute | Moyen | Prédiction ML 48h + collecte 30min |
| GPU insuffisant pour ConvLSTM | Moyenne | Élevé | Google Colab T4 gratuit |
| Décision React/Flutter non prise | Moyenne | Élevé | Deadline S2 imposée |
| n8n cloud limite gratuite | Faible | Faible | n8n self-hosted via Docker |
| Twilio sandbox expiration | Faible | Faible | Email en priorité absolue |
| Temps insuffisant pour U-Net | Haute | Faible | Optionnel — ne pas bloquer Must Have |

---

## 10. LIVRABLES FINAUX (23/05/2026)

| # | Livrable | Format |
|---|----------|--------|
| L1 | Ce Cahier des Charges | Markdown Obsidian |
| L2 | Repo GitHub (`madfire-platform`) | Code + notebooks + n8n JSON |
| L3 | `docker-compose up` fonctionnel | Docker |
| L4 | FastAPI déployée + Swagger UI | URL publique (Railway/Render gratuit) |
| L5 | Frontend déployé (Vercel ou Web) | URL publique |
| L6 | Modèle JeryMotroNet + métriques | Rapport PDF |
| L7 | Vidéo démo 3 minutes | MP4 |
| L8 | Mémoire L3 complet | PDF |
| L9 | Présentation soutenance | PowerPoint |

---

## 11. CLÉS API

| Service | Clé / Accès | Statut |
|---------|-------------|--------|
| NASA FIRMS | MAP_KEY (gratuite sur firms.modaps.eosdis.nasa.gov) | À obtenir S1 |
| NASA Earthdata | Token JWT (compte earthdata.nasa.gov) | Disponible |
| Groq API | `gsk_...` (fournie) | ✅ Disponible |
| Twilio Sandbox | Gratuit (compte twilio.com) | À créer S9 |
| Google Earth Engine | Compte académique gratuit | À créer S4 |

> ⚠️ **NE JAMAIS committer les clés dans GitHub.** Utiliser `.env` + `.gitignore`.

---

*Architecture → [[02_Architecture_Globale]]*
*Planning → [[03_Plan_Travail_3_Mois]]*
*Docker → [[08_Docker_Infrastructure]]*
*Backend → [[09_FastAPI_Backend]]*
*Frontend → [[10_Frontend_Decision]]*
