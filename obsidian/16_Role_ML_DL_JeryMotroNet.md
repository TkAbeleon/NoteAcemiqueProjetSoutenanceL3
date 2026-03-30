# 🧩 Rôle & Fonctionnement — ML vs DL (JeryMotro Platform)
#JeryMotro #MemoireL3 #ML #DL #Architecture #Workflow
[[Glossaire_Tags]] | [[00_INDEX]] | [[02_Architecture_Globale]] | [[04_MadFireNet]]

> Ce document explique **pourquoi** on utilise du Machine Learning (ML) et du Deep Learning (DL) dans JeryMotro, et **comment** ces blocs fonctionnent dans le pipeline.

---

## 1) Où se placent ML et DL dans le pipeline

Dans JeryMotro Platform, ML/DL ne sont pas “à côté” du projet : ils sont le **cœur** qui transforme des détections FIRMS brutes en **scores exploitables** (risque) et en **prédiction J+1**.

**Chaîne simplifiée :**
1. **FIRMS (MODIS/VIIRS)** → points (lat/lon/date/FRP/brightness/…)
2. **Prétraitement + Features** → variables explicatives (diff_brightness, frp_log, heure locale, saison sèche, ERA5…)
3. **Clustering (HDBSCAN)** → regroupe les points en *événements* (clusters)
4. **ML (XGBoost)** → score `risk_score` par point/cluster
5. **DL (ConvLSTM)** → carte de risque **spatio-temporelle** pour **J+1**
6. **Stockage + FastAPI** → endpoints consommés par le frontend + alertes

Références : [[06_Feature_Engineering]], [[05_HDBSCAN_Clustering]], [[09_FastAPI_Backend]], [[12_Systeme_Alertes]].

---

## 2) Pourquoi du ML (XGBoost) ?

### 2.0 C’est quoi “le ML” ici (concrètement) ?
Dans JeryMotro, la partie **ML** correspond à un **modèle de classification supervisée** (ou semi-supervisée) qui prend un **tableau de features** (1 ligne = 1 détection FIRMS) et renvoie un **score de risque**.

Intuition simple :
- *Entrée* : “Ce point est détecté à telle heure, avec tel FRP, telle signature thermique, dans tel contexte météo, dans tel cluster…”
- *Sortie* : “Ce point ressemble à un vrai feu ou plutôt à un bruit thermique ?” → `risk_score`.

### 2.0.1 Pourquoi XGBoost (au lieu d’un modèle plus simple) ?
XGBoost est adapté car :
- excellent sur **données tabulaires** (features hétérogènes : thermiques, météo, cluster)
- gère bien les **non-linéarités** et interactions (ex: *FRP élevé* + *saison sèche* + *vent fort*)
- robuste avec des **données imparfaites** (valeurs manquantes, bruit)
- rapide à entraîner et à déployer (un fichier `.pkl` suffit)

### 2.1 Rôle
Le ML sert à **améliorer la décision** au niveau des points FIRMS :
- FIRMS donne une *détection* + une *confiance* (souvent insuffisante pour une alerte fiable).
- Le ML combine **plus de signaux** (thermiques + météo + contexte de cluster) pour estimer un **risque** plus robuste.

### 2.2 Entrées (features)
Le classifieur ML prend typiquement :
- **FIRMS** : `brightness`, `bright_t31/ti5`, `frp`, `daynight`, `acq_time`, `confidence`
- **Transformations** : `diff_brightness`, `frp_log`, `local_hour`, `is_dry_season`, `scan_track_ratio`, `confidence_num`
- **Clusters** : `cluster_size`, `cluster_frp_total`, `cluster_frp_max`, `is_noise`
- **Météo (ERA5)** : température, humidité, vent, précipitations (via GEE)

Détail : [[06_Feature_Engineering]].

### 2.2.1 Exemple d’effet “valeur ajoutée ML”
Sans ML, tu pourrais faire des règles du type :
- “si `confidence` high et `frp > X` alors alerte”

Le ML apprend des règles **plus fines** :
- `diff_brightness` très élevé → feu probable même si `confidence` “nominal”
- même `frp`, mais **saison humide + humidité forte** → risque réel plus faible
- point isolé (`is_noise=1`) → souvent moins fiable qu’un point dans un cluster (`cluster_size` élevé)

### 2.3 Sorties
Le ML produit :
- `risk_score` ∈ [0, 1] (probabilité/score de risque)
- `fire_predicted` (0/1) selon un seuil (ex: 0.70)

Ces sorties alimentent :
- **FastAPI** : `GET /detections`, `GET /predictions`
- **Alertes** : déclenchement si `risk_score > 0.70` (voir [[12_Systeme_Alertes]])

### 2.4 Entraînement (logique)
Le point délicat : **absence de “ground truth terrain”** complet.
Approche utilisée dans les notes : **label semi-supervisé** basé sur des règles (confiance + FRP + saison) pour créer une cible d’entraînement, puis validation via métriques (AUC, F1, rappel) et comparaison “vs NASA brut”.

Référence : [[04_MadFireNet]] + tableau de suivi [[METRIQUES_CIBLES]].

### 2.4.1 Pipeline d’entraînement recommandé (étapes)
1. **Assembler** les données historiques (2020–2025) + features + clusters.
2. **Créer la cible** (`fire_label`) via règles semi-supervisées (voir [[04_MadFireNet]]).
3. **Découper train/val/test** avec une logique temporelle (ex: années 2020–2024 en train, 2025 en test) pour éviter de “tricher” sur le futur.
4. **Gérer le déséquilibre** feu/non-feu (souvent très déséquilibré) :
   - `scale_pos_weight` (ex: 15 dans les notes)
   - métriques orientées rappel/précision plutôt que “accuracy”
5. **Entraîner** avec `early_stopping_rounds` et une validation.
6. **Sauvegarder** le modèle (`.pkl`) + la liste `FEATURE_COLS` + la version (ex: `xgb_jerymotrnet_v1.pkl`).

### 2.4.2 Ce qu’il faut mesurer (et pourquoi)
Pour le mémoire, les métriques sont importantes car elles justifient que le ML “fait mieux” que FIRMS brut :
- **Recall** (rappel) : ne pas rater des feux (objectif +25% vs NASA brut)
- **Précision** : limiter les fausses alertes
- **AUC-ROC / F1** : qualité globale

Suivi : [[METRIQUES_CIBLES]].

### 2.4.3 Choix du seuil `risk_score` (0.70) = décision produit
Le seuil n’est pas “magique” : c’est un compromis **rappel vs fausses alertes**.
Dans le logiciel, tu peux l’expliquer comme :
- `risk_score > 0.70` → alerte (risque élevé)
- `0.50–0.70` → affichage sur carte / email seulement (risque modéré)

Référence : [[12_Systeme_Alertes]].

### 2.4.4 Interprétation (utile pour expliquer au jury)
Même si XGBoost est un “ensemble d’arbres”, on peut expliquer quelles variables comptent :
- importance des features (gain/weight)
- SHAP (si tu veux un graphique dans le mémoire)

Objectif : montrer que le modèle s’appuie sur des signaux cohérents (ex: `diff_brightness`, `frp_log`, saison sèche, variables météo), et pas sur du hasard.

### 2.4.5 Déploiement & maintenance (vision ingénierie)
En production, la partie ML doit être :
- **déterministe** : même input → même output (pipeline feature stable)
- **versionnée** : modèle + features + seuils (pour reproductibilité)
- **monitorée** : si la distribution des features change (capteurs, saisons, API), prévoir un **retrain** périodique (ex: mensuel/trimestriel) ou au moins une ré-évaluation.

---

## 3) Pourquoi du DL (ConvLSTM) ?

### 3.1 Rôle
Le DL sert à un besoin différent du ML :
- Le ML “juge” un point à un instant *t*.
- Le DL doit **modéliser une dynamique spatio-temporelle** : comment le risque évolue sur une grille et **prédire J+1**.

### 3.2 Pourquoi ConvLSTM (et pas un modèle tabulaire)
Une carte de risque est une donnée de type **image** (H×W) qui évolue dans le temps (séquence de plusieurs jours).
ConvLSTM combine :
- des convolutions (voisinage spatial : propagation locale)
- une mémoire temporelle (séquence sur 7 jours, par exemple)

### 3.3 Entrées / sorties
Entrée : un tenseur `seq_len × channels × H × W` (ex: 7 jours × plusieurs canaux : FRP, brightness, météo, saison…).

Sortie : une carte `1 × H × W` de probabilité/risque pour **J+1**.

Comme la grille complète de Madagascar est très grande, l’approche prévue est de travailler en **patches** (ex: 64×64) ou en résolution dégradée.

Référence : [[04_MadFireNet]].

---

## 4) Comment ML et DL s’intègrent au logiciel

### 4.1 Production de données exploitables
- **ML** : fournit des scores directement utilisables sur la carte (couleurs, filtres, classement).
- **DL** : fournit un *raster/heatmap* (carte risque) pour visualisation et anticipation.

### 4.2 API
Les résultats ML/DL sont exposés via FastAPI (design attendu) :
- `GET /detections` : points + score
- `GET /predictions` : sorties agrégées
- `GET /risk-map` : carte ConvLSTM (GeoJSON/JSON)

Référence : [[09_FastAPI_Backend]].

### 4.3 Alertes
Le système d’alertes consomme principalement :
- seuils sur `risk_score`
- seuils sur `frp`
- informations clusters (taille, FRP total)

Référence : [[12_Systeme_Alertes]] + automatisation [[11_Automatisation_n8n]].

---

## 5) Mesures & critères de réussite (ce que le jury attend)

Les métriques sont suivies dans [[METRIQUES_CIBLES]] :
- ML (XGBoost) : amélioration “vs NASA brut”, AUC, F1, rappel, précision
- DL (ConvLSTM) : MAE carte J+1, précision/rappel sur zones à risque
- Pipeline : latence totale (< 5 min) et latence alerte (< 30 min)

---

## 6) Limites à annoncer clairement (et comment les présenter)

- **Labels imparfaits** (semi-supervisés) : assumer et cadrer comme une stratégie réaliste vu le manque de vérité terrain.
- **Biais capteurs** : MODIS (1km) vs VIIRS (375m), différents formats de confiance.
- **Résolution météo ERA5** (~28km) : utile pour le contexte, pas pour du micro-local.
- **DL coûteux** (grille immense) : justifier l’approche en patches + entraînement Colab.

Ces points peuvent être transformés en “choix d’ingénierie” dans le mémoire : contraintes → design pragmatique.

---

## 7) Lecture recommandée (dans ce vault)
- Vision globale : [[01_Cahier_des_Charges]], [[02_Architecture_Globale]]
- Modèle : [[04_MadFireNet]]
- Features : [[06_Feature_Engineering]]
- Clustering : [[05_HDBSCAN_Clustering]]
- Backend : [[09_FastAPI_Backend]]
- Alertes : [[12_Systeme_Alertes]]
- Suivi : [[03_Plan_Travail_3_Mois]], [[METRIQUES_CIBLES]]
