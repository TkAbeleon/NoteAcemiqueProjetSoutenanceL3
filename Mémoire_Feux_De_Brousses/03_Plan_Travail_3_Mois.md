# 📅 Plan de Travail — 3 Mois
#FireProject #MemoireL3 #Avancement #Milestone
[[Glossaire_Tags]] | [[00_INDEX]]

---

> **Durée totale : 12 semaines (Février → Mai 2026)**
> **Répartition : 50% Technique | 30% Design Thinking | 20% Business Canvas + Pitch**

---

## 🗓️ VUE D'ENSEMBLE

| Mois | Semaines | Phase | Objectif principal |
|------|----------|-------|--------------------|
| Mois 1 | S1–S4 | Fondations | Environnement + Données + Baseline ML |
| Mois 2 | S5–S8 | Développement | Deep Learning + n8n + Automatisation |
| Mois 3 | S9–S12 | Finalisation | IA générative + Dashboard + Mémoire |

---

## 📦 MOIS 1 — FONDATIONS (S1–S4)

### 🗓️ Semaine 1 — Environnement & Infrastructure
#Milestone #DailyNote

**Objectif : Tout est installé et fonctionnel**

| Tâche | Durée | Tag |
|-------|-------|-----|
| Installer Python, Jupyter, bibliothèques SIG | 2h | #Python |
| Créer compte NASA Earthdata + obtenir MAP_KEY FIRMS | 1h | #API #NASA |
| Créer compte Copernicus / Sentinel Hub | 1h | #API #Sentinel2 |
| Installer n8n (Docker ou cloud) | 3h | #n8n |
| Installer Ollama + Llama 3 en local | 2h | #API |
| Configurer GitHub (repo FireProject) | 1h | #Python |
| Premier appel API FIRMS → vérifier données Madagascar | 2h | #FIRMS #Dataset |
| Créer vault Obsidian selon structure fournie | 1h | #Avancement |

**Livrable S1 :** Environnement 100% opérationnel, premier CSV FIRMS téléchargé

---

### 🗓️ Semaine 2 — Collecte & Exploration des Données
#Dataset #DataCleaning

**Objectif : Comprendre les données disponibles**

| Tâche | Durée | Tag |
|-------|-------|-----|
| Télécharger 1 an de données FIRMS MODIS pour Madagascar | 3h | #MODIS #Dataset |
| Télécharger 1 an de données FIRMS VIIRS pour Madagascar | 2h | #VIIRS #Dataset |
| Analyse exploratoire (EDA) : distribution, valeurs manquantes | 4h | #Python #DataCleaning |
| Visualisation géographique (carte des feux) avec Folium | 3h | #Python |
| Télécharger données Hansen GFC pour Madagascar | 2h | #Dataset |
| Documenter les datasets → [[08_Dataset_FIRMS_MODIS]] | 1h | #Dataset |
| Identifier les problèmes → [[PROB-001_Donnees_non_temps_reel]] | 1h | #Problem |

**Livrable S2 :** Notebook EDA complet, carte des feux 2023–2024 Madagascar

---

### 🗓️ Semaine 3 — Prétraitement & Feature Engineering
#DataCleaning #ML #Python

**Objectif : Données propres et features pertinentes**

| Tâche | Durée | Tag |
|-------|-------|-----|
| Filtrer les données par bounding box Madagascar | 1h | #DataCleaning |
| Nettoyer : doublons, valeurs aberrantes, types | 3h | #DataCleaning |
| Créer features temporelles (saison, mois, heure) | 2h | #ML |
| Créer features spatiales (région administrative) | 2h | #ML |
| Normaliser les variables numériques | 1h | #ML |
| Créer labels semi-supervisés (confidence > 80 = feu confirmé) | 2h | #Labelisation |
| Créer jeu train/val/test (70/15/15) | 1h | #ML |
| Documenter → [[08_Dataset_FIRMS_MODIS]] section Features | 1h | #Dataset |

**Livrable S3 :** Dataset propre + features + labels prêts pour ML

---

### 🗓️ Semaine 4 — Baseline ML (Random Forest)
#ML #Classification #Prediction

**Objectif : Premier modèle ML fonctionnel**

| Tâche | Durée | Tag |
|-------|-------|-----|
| Entraîner Random Forest (classification feu/non-feu) | 3h | #ML #Classification |
| Évaluer : accuracy, précision, rappel, F1, AUC-ROC | 2h | #ML |
| Visualiser feature importance | 1h | #ML |
| Entraîner XGBoost (comparaison) | 2h | #ML |
| Entraîner SVM (baseline) | 1h | #ML |
| Tableau comparatif des modèles ML | 1h | #ML |
| Sauvegarder le meilleur modèle (.pkl) | 1h | #ML |
| Documenter → [[TECH-001_Random_Forest]] | 1h | #ML |

**Livrable S4 :** Modèle ML baseline avec accuracy ≥ 80%, rapport comparatif

---

## 🔬 MOIS 2 — DÉVELOPPEMENT (S5–S8)

### 🗓️ Semaine 5 — Données Sentinel-2 & Indices Spectraux
#Sentinel2 #Dataset #Python

**Objectif : Intégrer les images satellitaires haute résolution**

| Tâche | Durée | Tag |
|-------|-------|-----|
| Configurer API Sentinel Hub (Copernicus) | 2h | #API #Sentinel2 |
| Télécharger images Sentinel-2 pour zones test (Menabe, Sofia) | 3h | #Dataset |
| Calculer NDVI (végétation) et NBR (zones brûlées) | 2h | #Python |
| Visualiser indices sur carte | 2h | #Python |
| Créer patches 64×64px pour entraînement DL | 3h | #DL #Dataset |
| Documenter → [[08_Dataset_Sentinel2]] | 1h | #Dataset |

**Livrable S5 :** Dataset images Sentinel-2 patchées + indices NDVI/NBR

---

### 🗓️ Semaine 6 — Deep Learning — CNN Classification
#DL #Classification

**Objectif : Premier modèle DL de classification d'images**

| Tâche | Durée | Tag |
|-------|-------|-----|
| Construire CNN baseline (4 couches conv + pooling) | 4h | #DL |
| Entraîner sur Google Colab GPU (T4) | 3h | #DL #Notebook |
| Évaluer : accuracy, matrice confusion | 2h | #DL |
| Essayer ResNet-18 (transfer learning depuis ImageNet) | 3h | #DL |
| Comparer CNN baseline vs ResNet | 1h | #DL |
| Documenter → [[TECH-003_CNN_Segmentation]] | 1h | #DL |

**Livrable S6 :** CNN fonctionnel, accuracy ≥ 82% sur images Sentinel-2

---

### 🗓️ Semaine 7 — Deep Learning — U-Net Segmentation
#DL #Classification

**Objectif : Segmentation pixel par pixel des zones brûlées**

| Tâche | Durée | Tag |
|-------|-------|-----|
| Construire U-Net (encodeur-décodeur + skip connections) | 5h | #DL |
| Créer masques de segmentation (zones brûlées / forêt / sol) | 3h | #Labelisation |
| Entraîner U-Net sur Colab GPU | 4h | #DL #Notebook |
| Évaluer : IoU (Intersection over Union), Dice Score | 2h | #DL |
| Visualiser prédictions vs masques réels | 1h | #DL |
| Documenter → [[TECH-005_UNet]] | 1h | #DL |

**Livrable S7 :** U-Net fonctionnel, IoU ≥ 0.65 (objectif : 0.70)

---

### 🗓️ Semaine 8 — Automatisation n8n + Pipeline Complet
#n8n #Workflow #Alerte

**Objectif : Pipeline end-to-end automatisé**

| Tâche | Durée | Tag |
|-------|-------|-----|
| Créer workflow n8n `daily_collection` (CRON → FIRMS API → CSV) | 4h | #n8n |
| Créer workflow n8n `ml_inference` (CSV → script Python → BDD) | 3h | #n8n #ML |
| Créer workflow n8n `alert_generator` (seuil → IA générative) | 3h | #n8n #Alerte |
| Tester pipeline complet de bout en bout | 2h | #Workflow |
| Créer BDD SQLite pour stocker historique détections | 2h | #Python |
| Documenter → [[07_Automatisation_n8n]] | 1h | #n8n |

**Livrable S8 :** Pipeline automatisé fonctionnel, collecte + inférence + alerte

---

## 🎯 MOIS 3 — FINALISATION (S9–S12)

### 🗓️ Semaine 9 — LSTM + Prédiction Temporelle
#DL #TimeSeries #Prediction

**Objectif : Anticiper les zones à risque 48–72h**

| Tâche | Durée | Tag |
|-------|-------|-----|
| Préparer séquences temporelles (fenêtre 7 jours) | 3h | #TimeSeries #DataCleaning |
| Construire LSTM (2 couches, 128 unités) | 3h | #DL |
| Entraîner LSTM sur historique feux Madagascar | 3h | #DL #Notebook |
| Évaluer : MSE, MAE, visualisation prédictions | 2h | #DL |
| Intégrer prédictions LSTM dans pipeline n8n | 2h | #n8n #Prediction |
| Documenter → [[TECH-004_LSTM_TimeSeries]] | 1h | #DL |

**Livrable S9 :** Modèle LSTM prédictif, intégré au pipeline

---

### 🗓️ Semaine 10 — IA Générative + Rapports Intelligents
#API #Alerte #DecisionSupport

**Objectif : Rapports en langage naturel pour décideurs**

| Tâche | Durée | Tag |
|-------|-------|-----|
| Construire prompt structuré (données ML → rapport) | 3h | #API |
| Intégrer Ollama (Llama 3) dans pipeline n8n | 3h | #n8n #API |
| Tester qualité des rapports générés | 2h | #Alerte |
| Configurer Groq API comme backup | 1h | #API |
| Créer rapport quotidien + rapport hebdomadaire | 2h | #Alerte #DecisionSupport |
| Générer rapport exemple pour le jury | 1h | #Soutenance |

**Livrable S10 :** Rapports IA générés automatiquement, intelligibles par non-technicien

---

### 🗓️ Semaine 11 — Dashboard & Visualisation
#Python #Monitoring #DecisionSupport

**Objectif : Interface visuelle pour les décideurs**

| Tâche | Durée | Tag |
|-------|-------|-----|
| Créer carte interactive avec Folium / Leaflet | 4h | #Python |
| Afficher détections du jour (points chauds colorés par FRP) | 2h | #Monitoring |
| Afficher prédictions zones à risque (heatmap) | 2h | #Prediction |
| Afficher évolution déforestation (comparaison annuelle) | 2h | #Monitoring |
| Intégrer carte dans rapport HTML automatique | 2h | #Workflow |
| Tester avec données réelles Madagascar | 1h | #Avancement |

**Livrable S11 :** Dashboard fonctionnel avec carte interactive

---

### 🗓️ Semaine 12 — Mémoire, Soutenance & Finalisation
#Soutenance #MemoireL3 #Milestone

**Objectif : Livrer un mémoire complet et une présentation convaincante**

| Tâche | Durée | Tag |
|-------|-------|-----|
| Rédiger/finaliser mémoire L3 (introduction, méthodologie, résultats) | 10h | #MemoireL3 |
| Créer présentation soutenance (slides) | 5h | #Soutenance |
| Préparer démo live (pipeline en direct) | 3h | #Soutenance |
| Répétition soutenance | 2h | #Soutenance |
| Créer README GitHub complet | 1h | #Python |
| Archiver vault Obsidian final | 1h | #Avancement |

**Livrable S12 :** Mémoire L3 + présentation + démo + code GitHub

---

## 📊 RÉCAPITULATIF DES LIVRABLES

| Semaine | Livrable clé | Priorité |
|---------|--------------|----------|
| S1 | Environnement opérationnel | 🔴 Critique |
| S2 | EDA + carte feux Madagascar | 🔴 Critique |
| S3 | Dataset propre + features | 🔴 Critique |
| S4 | Modèle Random Forest baseline | 🔴 Critique |
| S5 | Dataset Sentinel-2 | 🟠 Haute |
| S6 | CNN classification | 🟠 Haute |
| S7 | U-Net segmentation | 🟠 Haute |
| S8 | Pipeline n8n automatisé | 🔴 Critique |
| S9 | LSTM prédictif | 🟡 Moyenne |
| S10 | Rapports IA générative | 🔴 Critique |
| S11 | Dashboard visualisation | 🟠 Haute |
| S12 | Mémoire + soutenance | 🔴 Critique |

---

## ⚡ RÈGLES DE GESTION DU TEMPS

1. **Chaque jour** → remplir [[DailyNote_Template]] (10 min)
2. **Chaque semaine** → faire le point sur le livrable prévu
3. **Si retard** → sacrifier U-Net (S7) en premier, jamais le pipeline (S8)
4. **Si avance** → approfondir la validation terrain (zones connues)
5. **Backup GPU** → Google Colab si PC insuffisant pour DL

---

*Think Tank → [[02_Think_Tank]]*
*Architecture → [[04_Architecture_Globale]]*
