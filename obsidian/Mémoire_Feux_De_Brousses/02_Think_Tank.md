# 🧠 Think Tank — FireProject
#FireProject #ThinkTank #MemoireL3 #Soutenance
[[Glossaire_Tags]] | [[00_INDEX]]

---

> *Ce Think Tank est la BASE CENTRALE du projet. Tout découle de ce document.*

---

## 1. PROBLÈME STRATÉGIQUE (VALIDÉ)

Madagascar subit simultanément trois crises environnementales :

**Crise 1 — Feux de brousse incontrôlés**
Les feux progressent d'année en année. Les pratiques agricoles (tavy = culture sur brûlis) accentuent le phénomène. Sans système d'alerte précoce, les interventions arrivent toujours trop tard.

**Crise 2 — Déforestation rapide**
Madagascar a perdu plus de 40% de sa couverture forestière originelle. La forêt qui disparaît ne repousse pas à l'identique. La perte de biodiversité est irréversible à l'échelle humaine.

**Crise 3 — Données non exploitées**
Les satellites NASA et ESA passent au-dessus de Madagascar chaque jour. Les données sont publiques et gratuites. Pourtant, aucune chaîne locale ne les exploite de manière systématique, automatique et intelligente.

> **Constat clé :** Ce n'est pas un problème de données. C'est un problème de chaîne de traitement.

---

## 2. VISION DU THINK TANK

Créer un **hub d'intelligence environnementale** qui :

1. **Observe** automatiquement (APIs satellites)
2. **Analyse** scientifiquement (ML / DL)
3. **Structure** les résultats (base de données géospatiale)
4. **Orchestre** le flux (n8n)
5. **Interprète** en langage humain (IA générative)
6. **Agit** par alertes et rapports décisionnels

### Phrase clé pour le jury

> *"Transformer des données satellites ouvertes en intelligence environnementale actionnable, grâce à une synergie entre machine learning, deep learning, automatisation et intelligence artificielle générative."*

---

## 3. ARCHITECTURE GLOBALE (LOGIQUE CAUSALE)

La plateforme suit une chaîne causale stricte — chaque couche dépend de la précédente :

```
┌──────────────────────────────────────────────┐
│  COUCHE 1 : OBSERVATION (Données Factuelles) │
│  NASA FIRMS → MODIS NRT + VIIRS SNPP/NOAA   │
│  Copernicus → Sentinel-2 (10m résolution)    │
│  Hansen GFC → Déforestation historique       │
└─────────────────────┬────────────────────────┘
                      ↓
┌──────────────────────────────────────────────┐
│  COUCHE 2 : PRÉTRAITEMENT SIG                │
│  Python + Rasterio + GeoPandas + QGIS       │
│  → Filtrage bounding box Madagascar          │
│  → Calcul NDVI, NBR, indices spectraux       │
│  → Alignement temporel multi-capteurs        │
└─────────────────────┬────────────────────────┘
                      ↓
┌──────────────────────────────────────────────┐
│  COUCHE 3 : INTELLIGENCE ANALYTIQUE (ML/DL) │
│  ML : Random Forest, XGBoost, SVM           │
│  DL : CNN, U-Net, ResNet, LSTM              │
│  → Classification : feu / non-feu           │
│  → Segmentation : zones déforestées          │
│  → Prédiction : zones à risque 48–72h        │
└─────────────────────┬────────────────────────┘
                      ↓
┌──────────────────────────────────────────────┐
│  COUCHE 4 : STOCKAGE STRUCTURÉ               │
│  CSV / GeoJSON / SQLite / PostGIS            │
│  → Historique des détections                 │
│  → Scores ML, prédictions, métadonnées       │
└─────────────────────┬────────────────────────┘
                      ↓
┌──────────────────────────────────────────────┐
│  COUCHE 5 : ORCHESTRATION (n8n)              │
│  → Planification quotidienne (CRON)          │
│  → Appels APIs, scripts Python, DL           │
│  → Mise à jour BDD + déclenchement alertes  │
└─────────────────────┬────────────────────────┘
                      ↓
┌──────────────────────────────────────────────┐
│  COUCHE 6 : IA GÉNÉRATIVE                    │
│  Ollama (local) → Llama 3 / Mistral          │
│  Groq API (backup rapide)                    │
│  → Résumés quotidiens en malgache/français   │
│  → Rapports régionaux détaillés              │
│  → Réponses aux questions décisionnelles     │
└─────────────────────┬────────────────────────┘
                      ↓
┌──────────────────────────────────────────────┐
│  COUCHE 7 : SORTIE DÉCISIONNELLE             │
│  → Dashboard Web (Leaflet / Folium)          │
│  → Alertes email/SMS automatiques            │
│  → Rapports PDF hebdomadaires                │
│  → API REST pour partenaires                 │
└──────────────────────────────────────────────┘
```

---

## 4. RÔLE EXACT DE CHAQUE COMPOSANT

### 4.1 APIs Satellites — Couche Factuelle Pure

> ⚠️ Aucune IA ici. Uniquement des faits bruts.

| API | Ce qu'elle donne | Fréquence |
|-----|-----------------|-----------|
| NASA FIRMS MODIS NRT | Détections thermiques, positions GPS, FRP | Toutes les ~3h |
| NASA FIRMS VIIRS SNPP | Détections plus précises (375m), confiance | Toutes les ~1.5h |
| NASA FIRMS VIIRS NOAA-20 | Deuxième passage VIIRS, couverture accrue | Toutes les ~1.5h |
| Copernicus Sentinel-2 | Images multibandes 10m, NDVI, NBR | Tous les 5 jours |
| Hansen GFC | Perte forestière annuelle 2000–présent | Annuel |

**Variables clés FIRMS à conserver :**
- `latitude`, `longitude` → position GPS
- `brightness` → température de brillance (Kelvin)
- `frp` → Fire Radiative Power (MW) — intensité réelle du feu
- `confidence` → niveau de confiance (0–100 ou low/nominal/high)
- `acq_date`, `acq_time` → horodatage acquisition
- `daynight` → D (jour) ou N (nuit)
- `satellite` → Terra, Aqua, SNPP, NOAA-20

**Bounding Box Madagascar :**
```
west=43.0, south=-25.6, east=50.5, north=-11.9
```

---

### 4.2 ML/DL — Couche Intelligence Analytique

#### Machine Learning (Socle — Phase 1)

**Random Forest** *(priorité absolue)*
- Entrées : brightness, frp, confidence, NDVI, saison, région
- Sortie : feu_confirmé (0/1) + score de risque (0–1)
- Avantage : interprétable, robuste aux données manquantes
- Référence → [[TECH-001_Random_Forest]]

**XGBoost** *(Phase 2)*
- Entrées : idem + historique des 7 derniers jours
- Sortie : prédiction zone à risque 48–72h à l'avance
- Référence → [[TECH-002_XGBoost]]

**SVM** *(comparaison/validation)*
- Baseline de comparaison pour le mémoire

#### Deep Learning (Évolution — Phase 2–3)

**CNN** *(classification d'images)*
- Entrées : patches d'images Sentinel-2 (64×64px, 10m)
- Sortie : classe feu / cicatrice / forêt / sol nu
- Référence → [[TECH-003_CNN_Segmentation]]

**U-Net** *(segmentation sémantique)*
- Architecture encodeur-décodeur avec skip connections
- Sortie : masque pixel par pixel des zones brûlées/déforestées
- Référence → [[TECH-005_UNet]]

**LSTM** *(séries temporelles)*
- Entrées : séquences temporelles NDVI + FRP + météo
- Sortie : probabilité d'incendie dans les 48–72h
- Référence → [[TECH-004_LSTM_TimeSeries]]

---

### 4.3 n8n — Cerveau Opérationnel

> n8n relie TOUTES les couches. C'est le chef d'orchestre.

**Workflows principaux :**

| Workflow | Déclencheur | Actions |
|----------|-------------|---------|
| `daily_collection` | CRON 06h00 | Appel FIRMS API → CSV → BDD |
| `ml_inference` | Après collection | Script Python ML → scores → BDD |
| `alert_generator` | Si score > seuil | Appel IA générative → email/SMS |
| `weekly_report` | CRON lundi 08h00 | Agrégation + rapport PDF + envoi |
| `sentinel_sync` | CRON tous les 5j | Téléchargement nouvelles images S2 |

*Détails → [[07_Automatisation_n8n]]*

---

### 4.4 IA Générative — Couche Interprétation

> ⚠️ L'IA générative n'invente rien. Elle interprète les résultats ML/DL.

**Ce qu'elle reçoit (prompt structuré) :**
```
Données du jour pour Madagascar :
- 47 détections de feux (FIRMS VIIRS)
- Zones les plus touchées : Menabe (23 feux), Sofia (12 feux)
- FRP moyen : 145 MW (intensité élevée)
- Confiance moyenne : 78%
- Modèle ML : 3 zones à risque élevé dans les 48h

Génère un rapport d'alerte en français pour les décideurs.
```

**Ce qu'elle produit :**
Un rapport structuré, lisible, avec recommandations, en français ou malgache.

**Options IA générative (par ordre de priorité) :**
1. **Ollama local** → Llama 3 8B ou Mistral 7B (gratuit, souverain, illimité)
2. **Groq API** → `llama3-8b-8192` (très rapide, quota généreux)
3. **Hugging Face** → `mistralai/Mistral-7B-Instruct` (backup)

---

## 5. RESSOURCES DU THINK TANK

### Humaines (priorité absolue)

| Rôle | Mission | Disponibilité |
|------|---------|---------------|
| Porteur du projet | Dev IA, pipeline, mémoire | 100% |
| Expert environnement | Validation scientifique terrain | Consultatif |
| Encadrante Mme Larissa | Orientation académique | Hebdomadaire |
| Acteurs locaux | Validation sur zones connues | Ponctuel |

### Financières

> **Principe fort : On peut commencer sans argent, mais pas sans structure.**

- Phase 1 : 0 Ar — tout gratuit (APIs NASA, Colab, Ollama)
- Phase 2 : VPS léger optionnel (~10–20 USD/mois si déploiement)
- Phase 3 : Financement ONG / État si validation terrain

### Matérielles

| Ressource | Usage |
|-----------|-------|
| PC personnel | Développement, ML local, n8n |
| Google Colab (gratuit) | Entraînement DL (GPU T4) |
| Internet | APIs, GitHub, documentation |
| GitHub | Versioning, collaboration |

---

## 6. POSITIONNEMENT STRATÉGIQUE

Ce Think Tank se positionne comme :

- Un **hub d'intelligence environnementale** à Madagascar
- Une **preuve que l'IA peut servir localement** avec zéro budget
- Une **base scientifique évolutive** (prototype → startup → ONG tech)
- Un **outil d'aide à la décision** (pas de remplacement humain)

### Différenciation par rapport à l'existant

| Existant | FireProject |
|----------|-------------|
| FIRMS seul : données brutes | FIRMS + ML/DL : données analysées |
| AFIS : limité à l'Afrique du Sud | Adapté spécifiquement à Madagascar |
| Outils globaux non localisés | Adapté au contexte malgache |
| Pas d'IA générative | Rapports en langue locale |

---

## 7. BOUCLE D'AMÉLIORATION (DESIGN THINKING)

```
INSPIRATION → IMAGINATION → IMPLÉMENTATION → AMÉLIORATION → (retour)
    ↓               ↓              ↓                ↓
Besoins       Architecture     Prototype         Tests terrain
terrain       technique        ML/DL             + feedback
```

---

*Plan de travail → [[03_Plan_Travail_3_Mois]]*
*Architecture détaillée → [[04_Architecture_Globale]]*
*APIs → [[05_APIs_et_Donnees]]*
