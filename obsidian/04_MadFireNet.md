# 🚀 JeryMotroXGB — Documentation Complète du Modèle Classification
#JeryMotro #MemoireL3 #XGBoost #Classification #ML
[[Glossaire_Tags]] | [[00_INDEX]] | [[06_Feature_Engineering]]

---

> **JeryMotroXGB** (Branche A de JeryMotroNet) est un modèle de Machine Learning avancé (XGBoost) conçu pour évaluer précisément le niveau de risque et la véracité d'une anomalie thermique détectée à Madagascar.
> 
> Son innovation réside dans son **intelligence contextuelle** : il ne regarde pas seulement l'intensité du feu brut, mais le croise avec la couverture forestière, la météo, la topographie et l'historique de déforestation.

---

## 1. ARCHITECTURE DES DONNÉES (HYBRIDE)

Le dataset qui nourrit JeryMotroXGB est construit via une architecture hybride, combinant la puissance d'archivage de la NASA avec l'intelligence temps réel de GEE :

1. ** NASA Earthdata Token (`earthaccess`)** : Utilisé pour télécharger massivement les archives historiques HDF4 (ex: `MOD14A1`) sur la période 2021-2024. C'est la base de l'entraînement.
2. ** Google Earth Engine (Python API)** : Utilisé pour le calcul à la volée du contexte géographique autour du feu, sans avoir besoin de télécharger les images satellites sous-jacentes.

---

## 2. SCHEMA D'ENTRÉE : LES 20 FEATURES

Le modèle prend exactement un vecteur de dimension 20 en entrée.

### Groupe 1 : Caractéristiques Physiques (NASA FIRMS)
| Feature | Type | Description |
|---------|------|-------------|
| `diff_brightness` | Float | Différence de température Brillance vs Fond (K) |
| `frp_log` | Float | `log1p(frp)` — Puissance radiative du feu (MW) |
| `brightness` | Float | Température absolue en Kelvin |
| `local_hour` | Int | Heure EAT locale (capture du cycle diurne) |
| `is_dry_season` | Int | `1` si mois = [Avr-Oct], `0` sinon |
| `daynight_bin` | Int | D=1, N=0 |
| `confidence_num` | Int | Confiance algorithmique NASA (0-100) |
| `scan_track_ratio` | Float | Distorsion géométrique du pixel (effets de bord) |

### Groupe 2 : Contexte Spatial (HDBSCAN Clustering)
| Feature | Type | Description |
|---------|------|-------------|
| `cluster_size` | Int | Nombre de points actifs ensemble (dans 750m) |
| `cluster_frp_total` | Float | Énergie libérée totale du cluster |
| `cluster_frp_max` | Float | Pic d'énergie du cluster |
| `is_noise` | Int | `1` si le feu est isolé (aberration probable) |

### Groupe 3 : Intelligence Environnementale (via GEE)
| Feature | Source | Importance pour le ML |
|---------|--------|----------------------|
| `temperature_2m`| ERA5 | Favorise l'inflammation spontanée |
| `relative_humidity`| ERA5 | Assèchement du sol (combustible sec) |
| `wind_speed`| ERA5 | Force la propagation et l'intensité en MW |
| `landcover`| ESA 10m | Distingue un feu de savane d'un feu de forêt primaire |
| `slope_deg`| NASADEM | Une forte pente draine l'humidité et propage le feu plus vite |
| `ndvi_10m`| Sentinel-2 | Valeur exacte à 10m de résolution de la biomasse végétale verte |
| `is_recent_loss`| Hansen GFC| `1` si = zone récemment déforestée (Indicateur critique de brûlis agricole / Tavy) |

---

## 3. LOGIQUE SEMI-SUPERVISÉE DU LABEL

Puisqu'il n'existe pas de base de "vérité terrain" (Ground Truth) exhaustive pour les feux à Madagascar, l'entraînement de JeryMotroXGB utilise une méthode **heuristique de labellisation forte**.

```python
def generate_ground_truth_proxy(df):
    """Génère la cible (y) pour l'entraînement."""
    df['fire_label'] = 0
    
    # 1. Feu Fortement Confirmé
    df.loc[(df['confidence_num'] >= 85) & (df['frp'] > 15), 'fire_label'] = 1
    
    # 2. Feu Contexte Agricole Corroboré (L'intelligence du modèle)
    df.loc[
        (df['confidence_num'] >= 60) & 
        (df['frp'] > 8) & 
        (df['is_dry_season'] == 1) & 
        (df['is_recent_loss'] == 1), # Brûlis typique
        'fire_label'
    ] = 1
    
    return df
```

---

## 4. MODÈLE & HYPERPARAMÈTRES OPTIMISÉS

Le modèle utilise `xgboost.XGBClassifier` optimisé pour la vitesse d'inférence et la robustesse face au déséquilibre des classes (scale_pos_weight).

```python
import xgboost as xgb

jerymotro_xgb = xgb.XGBClassifier(
    n_estimators=700,          # Forêt dense pour capturer les 20 features
    max_depth=8,               # Profondeur suffisante pour les interactions complexes
    learning_rate=0.02,        # Apprentissage lent/précis
    subsample=0.8,             # Prévention overfitting (row wise)
    colsample_bytree=0.8,      # Prévention overfitting (feature wise)
    min_child_weight=7,        # Évite les feuilles trop spécifiques
    scale_pos_weight=12,       # Compense le ratio (10 faux positifs pour 1 vrai feu)
    eval_metric=['auc', 'logloss'],
    early_stopping_rounds=40,
    random_state=42,
    tree_method='hist'         # Accélération drastique sur gros volumes (2021-2024)
)
```

---

## 5. INTERPRÉTATION EN PRODUCTION (INFÉRENCE NRT)

En temps réel (NRT via n8n CRON), dès que le script récupère un nouveau CSV FIRMS, le pipeline tourne pour enrichir le point avec GEE.
Ensuite, JeryMotroXGB sort une prédiction probabiliste : `predict_proba(X)[:, 1]`.

Cette probabilité devient le **`risk_score`**.

**Matrice de Décision Alertes JeryMotro :**

| `risk_score` | Interprétation | Action du Système |
|--------------|----------------|-------------------|
| **0.0 - 0.39** | Bruit thermique / Soleil réverbérant | Stocké en DB pour archives, ignoré |
| **0.40 - 0.69**| Feu suspect (Petit brûlis très isolé) | Stocké en DB, affiché sur carte en Jaune |
| **0.70 - 0.89**| **Feu Avéré Majeur** | **ALERTE DÉCLENCHÉE** (Email/Dashboard) |
| **0.90 - 1.00**| **Incendie Critique (FRP extrème)** | **ALERTE URGENCE** (WhatsApp + Email) |

---

## 6. MÉTRIQUES DE VALIDATION CIBLES (SUR JEU 2025)

L'évaluation définitive du mémoire L3 se fera sur les données de l'année complète 2025 (Test Out-Of-Distribution) non vues pendant l'entraînement :

- **Recall (Rappel) : ≥ +25%** par rapport à l'utilisation du filtre "High Confidence" de la NASA seul. Le modèle doit rattraper les petits feux de forêt que la NASA classe comme "Low" mais que le contexte (NDVI + HDBSCAN + ERA5) prouve être réels.
- **AUC-ROC : ≥ 0.88**.
- **Précision : ≥ 80%**. Moins de 20% de fausses alertes pour ne pas harceler les utilisateurs du système d'alerte.

---

*Feature Engineering Détails → [[06_Feature_Engineering]]*
*Automatisation Temps Réel → [[11_Automatisation_n8n]]*
*Backend FastAPI → [[09_FastAPI_Backend]]*
