# 📅 Plan de Travail — 3 Mois (S1→S12)
#JeryMotro #MemoireL3 #Avancement #Milestone
[[Glossaire_Tags]] | [[00_INDEX]] | [[01_Cahier_des_Charges]]

> **Durée : 23/02/2026 → 23/05/2026**
> **Jalon hebdomadaire obligatoire :** 1 commit GitHub + [[DailyNote_Template]] + test pipeline

---

## 📦 MOIS 1 — FONDATION (S1–S4)
### Objectif : Infrastructure opérationnelle + données prêtes + EDA + Clustering

---

### 🗓️ S1 — Infrastructure & Mise en place (23/02 → 01/03)
#Milestone

**Objectif : Tout l'environnement est installé et fonctionnel**

| Tâche                                                               | Durée | Priorité |
| ------------------------------------------------------------------- | ----- | -------- |
| Créer repo GitHub `jery-motro-platform` + structure dossiers        | 1h    | 🔴       |
| Installer Docker Desktop + tester `docker run hello-world`          | 1h    | 🔴       |
| Écrire `docker-compose.yml` minimal (API + DB + ChromaDB)           | 3h    | 🔴       |
| Créer Dockerfile FastAPI (python:3.11-slim)                         | 2h    | 🔴       |
| Obtenir MAP_KEY NASA FIRMS (inscription gratuite)                   | 30min | 🔴       |
| Premier appel API FIRMS → vérifier CSV Madagascar                   | 1h    | 🔴       |
| Créer fichier `.env.example` + `.gitignore`                         | 30min | 🔴       |
| Installer Obsidian + importer ce vault                              | 30min | 🔴       |
| **Décision React vs Flutter** → noter dans [[10_Frontend_Decision]] | 1h    | 🔴       |

**Livrable S1 :** `docker-compose up` lance API + DB + ChromaDB. Premier CSV FIRMS téléchargé.

---

### 🗓️ S2 — Collecte Automatisée + n8n (02/03 → 08/03)
#API #n8n

**Objectif : Pipeline collecte FIRMS → PostgreSQL automatisé toutes les 30 min**

| Tâche | Durée | Priorité |
|-------|-------|----------|
| Écrire `fetch_firms.py` (3 sources : MODIS + VIIRS SNPP + VIIRS NOAA21) | 3h | 🔴 |
| Écrire `clean_firms.py` (filtres confidence, frp, doublons) | 2h | 🔴 |
| Créer modèle SQLAlchemy `Detection` + migration Alembic | 2h | 🔴 |
| Créer endpoint FastAPI `GET /detections` (basique) | 2h | 🔴 |
| Installer n8n Docker + créer workflow `daily_collection` (CRON 30min) | 3h | 🔴 |
| Configurer Dockerfile Frontend (selon décision S1) | 2h | 🟠 |
| Tester pipeline collecte bout-en-bout | 1h | 🔴 |

**Livrable S2 :** Données FIRMS dans PostgreSQL toutes les 30 min, endpoint `/detections` fonctionnel.

---

### 🗓️ S3 — EDA Complète (09/03 → 15/03)
#Dataset #DataCleaning #Notebook

**Objectif : Comprendre parfaitement les données Madagascar 2020–2025**

| Tâche | Durée | Priorité |
|-------|-------|----------|
| Télécharger archives FIRMS 2020–2025 pour Madagascar | 3h | 🔴 |
| `01_EDA_FIRMS.ipynb` : stats descriptives complètes | 4h | 🔴 |
| Visualisation temporelle : feux par mois/année/heure | 2h | 🔴 |
| Visualisation spatiale : carte densité feux avec Folium | 2h | 🔴 |
| Comparaison MODIS vs VIIRS (différences de détection) | 2h | 🟠 |
| Identifier régions les plus touchées (top 5) | 1h | 🔴 |
| Documenter → [[13_Dataset_FIRMS_MODIS]] + [[14_Dataset_FIRMS_VIIRS]] | 1h | 🔴 |

**Livrable S3 :** Notebook EDA complet, carte feux 2020–2025, rapport comparaison MODIS/VIIRS.

---

### 🗓️ S4 — Feature Engineering + HDBSCAN Clustering (16/03 → 22/03)
#ML #DataCleaning #Clustering

**Objectif : Données enrichies + premier clustering spatio-temporel**

| Tâche | Durée | Priorité |
|-------|-------|----------|
| `feature_engineering.py` : diff_brightness, frp_log, local_hour, is_dry_season | 3h | 🔴 |
| Configurer Google Earth Engine API (données ERA5) | 2h | 🟠 |
| `hdbscan_cluster.py` : rayon 750m, fenêtre 48h, min_cluster=3 | 4h | 🔴 |
| Évaluer qualité clusters (silhouette score, visualisation) | 2h | 🔴 |
| Ajouter cluster_features dans schéma PostgreSQL | 1h | 🔴 |
| Endpoint FastAPI `GET /clusters` | 2h | 🔴 |
| Documenter → [[05_HDBSCAN_Clustering]] + [[06_Feature_Engineering]] | 1h | 🔴 |

**Livrable S4 :** Dataset enrichi + clusters HDBSCAN validés + endpoint `/clusters` fonctionnel.

---

## 🔬 MOIS 2 — MODÉLISATION & INTERFACE (S5–S8)
### Objectif : JeryMotroNet + FastAPI complète + Frontend fonctionnel

---

### 🗓️ S5–S6 — JeryMotroNet : XGBoost + ConvLSTM (23/03 → 05/04)
#ML #DL #Notebook

**Objectif : Modèle JeryMotroNet entraîné et évalué**

| Tâche | Durée | Priorité |
|-------|-------|----------|
| `02_Feature_Engineering.ipynb` : pipeline features complet | 3h | 🔴 |
| `03_XGBoost_Training.ipynb` : entraîner + évaluer + sauvegarder | 5h | 🔴 |
| `xgboost_classifier.py` : classe `JeryMotroXGB` réutilisable | 2h | 🔴 |
| Construire grille 375m pour Madagascar | 3h | 🔴 |
| `04_ConvLSTM_Training.ipynb` : architecture + entraînement Colab GPU | 6h | 🔴 |
| `convlstm_predictor.py` : classe `JeryMotroConvLSTM` | 3h | 🔴 |
| `run_madfirenet.py` : pipeline inférence unified | 2h | 🔴 |
| Endpoints FastAPI : `GET /predictions`, `GET /risk-map` | 2h | 🔴 |
| Tableau métriques comparatif vs NASA brut | 2h | 🔴 |

**Livrable S5–S6 :** JeryMotroNet entraîné, recall petits feux +25%, endpoints `/predictions` et `/risk-map`.

---

### 🗓️ S7 — FastAPI Complète + Frontend Démarrage (06/04 → 12/04)
#FastAPI #Frontend

**Objectif : FastAPI complète avec Swagger + Frontend premier écran**

| Tâche | Durée | Priorité |
|-------|-------|----------|
| Compléter tous les endpoints FastAPI (avec schemas Pydantic) | 4h | 🔴 |
| Ajouter CORS, gestion erreurs, logs structurés | 2h | 🔴 |
| Tests unitaires FastAPI (pytest + httpx, ≥ 60% coverage) | 3h | 🔴 |
| **React** : scaffold `npx create-react-app` + Dockerfile | 2h | 🔴 |
| Composant `MapView.jsx` avec Leaflet (points feux sur carte) | 4h | 🔴 |
| Composant `Dashboard.jsx` graphiques saisonniers (Recharts) | 3h | 🟠 |
| Service `api.js` : tous les appels FastAPI | 2h | 🔴 |

**Livrable S7 :** FastAPI 100% documentée (Swagger) + carte interactive frontend affichant les feux réels.

---

### 🗓️ S8 — Frontend Complet + JeryMotro AI (13/04 → 19/04)
#Frontend #RAG #API

**Objectif : Interface complète + chat IA fonctionnel**

| Tâche | Durée | Priorité |
|-------|-------|----------|
| Composant `ChatPanel.jsx` (interface chat JeryMotro AI) | 3h | 🔴 |
| Composant `AlertPanel.jsx` (historique alertes) | 2h | 🔴 |
| `rag_service.py` : ChromaDB + Groq API + prompt engineering | 4h | 🔴 |
| Endpoint FastAPI `POST /chat` complet | 2h | 🔴 |
| Intégrer carte risque ConvLSTM J+1 dans frontend | 3h | 🟠 |
| Finaliser docker-compose avec tous les services | 2h | 🔴 |
| Test intégration complète bout-en-bout | 2h | 🔴 |

**Livrable S8 :** Frontend complet fonctionnel + JeryMotro AI chat opérationnel + docker-compose finalisé.

---

## 🎯 MOIS 3 — FINALISATION (S9–S12)
### Objectif : Alertes + Tests + Optionnel + Mémoire + Soutenance

---

### 🗓️ S9–S10 — Alertes + Tests End-to-End (20/04 → 03/05)
#Alertes #Tests

**Objectif : Système d'alertes fonctionnel + pipeline testé de bout en bout**

| Tâche | Durée | Priorité |
|-------|-------|----------|
| `alert_service.py` : email SMTP + WhatsApp Twilio Sandbox | 4h | 🔴 |
| Workflow n8n `alert_trigger` (IF score > 0.7 OU FRP > 50MW) | 3h | 🔴 |
| Tests alertes simulées (Twilio sandbox) | 2h | 🔴 |
| Tests end-to-end pipeline complet (collecte → alerte) | 4h | 🔴 |
| Mesurer toutes les métriques (latence, recall, silhouette) | 3h | 🔴 |
| Random Forest régression (prédiction durée cluster) — Should Have | 3h | 🟠 |
| Export PDF rapport quotidien — Should Have | 3h | 🟠 |

**Livrable S9–S10 :** Alertes opérationnelles + toutes métriques mesurées + rapport de tests.

---

### 🗓️ S11 — Option Images + Déploiement (04/05 → 10/05)
#Optional #Déploiement

**Objectif : Optionnel images satellites + déploiement public**

| Tâche | Durée | Priorité |
|-------|-------|----------|
| **Optionnel** : GEE → patches 128×128 → U-Net simple | 8h | 🟡 |
| Déployer FastAPI sur Railway/Render (gratuit) | 2h | 🟠 |
| Déployer Frontend sur Vercel (gratuit) | 2h | 🟠 |
| Créer README.md complet avec badges + screenshots | 3h | 🔴 |
| Exporter workflows n8n en JSON pour GitHub | 1h | 🔴 |

**Livrable S11 :** URLs publiques FastAPI + Frontend + README complet.

---

### 🗓️ S12 — Mémoire + Soutenance (11/05 → 23/05)
#Soutenance #MemoireL3

**Objectif : Livrer un mémoire L3 exceptionnel + présentation convaincante**

| Tâche | Durée | Priorité |
|-------|-------|----------|
| Rédiger mémoire L3 (introduction, état de l'art, méthodo, résultats) | 12h | 🔴 |
| Créer présentation soutenance (15–20 slides) | 5h | 🔴 |
| Enregistrer vidéo démo 3 minutes | 2h | 🔴 |
| Répétition soutenance à voix haute | 2h | 🔴 |
| Finaliser vault Obsidian (toutes les notes) | 2h | 🔴 |
| Dernier commit GitHub + tag `v1.0.0` | 30min | 🔴 |

**Livrable S12 :** Mémoire PDF + présentation + vidéo démo + code GitHub tagué.

---

## 📊 RÉCAPITULATIF DES LIVRABLES

| Semaine | Livrable | Statut |
|---------|---------|--------|
| S1 | docker-compose opérationnel + CSV FIRMS | ⬜ |
| S2 | Pipeline collecte automatisée | ⬜ |
| S3 | Notebook EDA complet | ⬜ |
| S4 | HDBSCAN + features + endpoint /clusters | ⬜ |
| S5–S6 | JeryMotroNet (XGBoost + ConvLSTM) entraîné | ⬜ |
| S7 | FastAPI Swagger + frontend carte | ⬜ |
| S8 | Frontend complet + JeryMotro AI | ⬜ |
| S9–S10 | Alertes + tests E2E | ⬜ |
| S11 | Déploiement public + README | ⬜ |
| S12 | Mémoire + soutenance | ⬜ |

---

## ⚡ RÈGLES DU PROJET

1. **Chaque jour** → remplir [[DailyNote_Template]] (10 min max)
2. **Chaque semaine** → 1 commit GitHub avec message clair
3. **Décision React/Flutter** → obligatoirement prise avant fin S1
4. **Si retard** → sacrifier S11 (optionnel), jamais S4 (clustering) ni S6 (JeryMotroNet)
5. **Clés API** → toujours dans `.env`, jamais dans le code

---

*Cahier des charges → [[01_Cahier_des_Charges]]*
*Architecture → [[02_Architecture_Globale]]*
