# 🤖 JeryMotroNet — Vue d'ensemble du Modèle
#JeryMotro #MemoireL3 #ML #DL #Classification #Prediction
[[Glossaire_Tags]] | [[00_INDEX]] | [[04_MadFireNet]] | [[06_Feature_Engineering]]

---

> **JeryMotroNet** est le modèle ML/DL original du projet JeryMotro.
> C'est la **contribution académique centrale** du mémoire L3.
> Deux branches : XGBoost (classification risque) + ConvLSTM (prédiction carte J+1)

---

## 1. POSITIONNEMENT

JeryMotroNet n'est **pas** un simple wrapper de NASA FIRMS.
Son objectif est de **corriger et enrichir** la confiance NASA en exploitant :
- Les features physiques des feux (thermique, FRP)
- Le contexte spatial (clusters HDBSCAN)
- La météo (ERA5 via GEE)
- Le contexte environnemental V2 : Landcover · Pente · NDVI

```
NASA FIRMS seul       → recall ~60% (beaucoup de petits feux manqués)
JeryMotroNet V2       → recall cible ≥ 85% (+25% minimum)
```

---

## 2. DEUX BRANCHES

| Branche | Modèle | Entrée | Sortie |
|---------|--------|--------|--------|
| **A** | XGBoost | 18 features (FIRMS + HDBSCAN + GEE) | `fire_risk` (0/1) + `risk_score` (0.0–1.0) |
| **B** | ConvLSTM | Séries 7j sur grille 375m (patches 64×64) | Carte risque J+1 (probabilité 0.0–1.0) |

---

## 3. FEATURES D'ENTRÉE (Version V2 — 18 features)

### Groupe 1 : FIRMS (données satellites brutes)
| Feature | Description |
|---------|-------------|
| `diff_brightness` | `brightness - bright_t31` — différence thermique feu/fond |
| `frp_log` | `log1p(frp)` — puissance rayonnée (normalisée) |
| `brightness` | Température de brillance (K) |
| `local_hour` | Heure locale EAT (UTC+3) |
| `is_dry_season` | 1 si mois ∈ {4..10} (saison sèche Madagascar) |
| `daynight_bin` | Jour=1, Nuit=0 |
| `confidence_num` | high=90 / nominal=65 / low=30 |
| `scan_track_ratio` | Distorsion géométrique du capteur |

### Groupe 2 : HDBSCAN (contexte spatial)
| Feature | Description |
|---------|-------------|
| `cluster_size` | Nombre de points dans la grappe |
| `cluster_frp_total` | FRP total du cluster (MW) |
| `cluster_frp_max` | FRP max dans le cluster |
| `is_noise` | 1 si point isolé (cluster_id = -1) |

### Groupe 3 : GEE — Météo + Contexte (V2)
| Feature | Source | Description |
|---------|--------|-------------|
| `temperature_2m` | ERA5 | Température air (°C) |
| `relative_humidity` | ERA5 | Humidité relative (%) |
| `wind_speed` | ERA5 | Vitesse vent (m/s) |
| `landcover` | ESA WorldCover | Classe d'occupation du sol |
| `slope_deg` | NASADEM | Pente topographique (°) |
| `ndvi_pre_fire` | MODIS | NDVI 30 jours avant détection |

---

## 4. STRATÉGIE D'ENTRAÎNEMENT

| Période | Rôle | Volume estimé |
|---------|------|---------------|
| 2021 – 2024 | Train + CV (80/20 interne) | ~500k détections |
| 2025 | Validation OOD (out-of-distribution) | ~120k détections |
| 2026 | Inférence temps réel | continu |

> [!important] Sensibilité saisonnière
> Les feux malgaches ont un pic juillet–novembre.
> Inclure au moins 4 saisons sèches dans le train est **obligatoire**.

---

## 5. MÉTRIQUES CIBLES

| Métrique | Cible | Seuil minimal acceptable |
|----------|-------|--------------------------|
| **Recall** (feux réels) | ≥ +25% vs NASA brut | +15% |
| **Précision** | ≥ 80% | ≥ 70% |
| **AUC-ROC** | ≥ 0.88 | ≥ 0.82 |
| **F1-Score** | ≥ 0.80 | ≥ 0.75 |
| **MAE ConvLSTM J+1** | < 0.15 | < 0.20 |

---

## 6. DOCUMENTATION DÉTAILLÉE

- Détail XGBoost (code + hyperparamètres + labeling) → [[04_MadFireNet]]
- Features complètes + pipeline → [[06_Feature_Engineering]]
- GEE enrichissement V2 → [[15_Dataset_ERA5_GEE]]
- Clustering contextuel → [[05_HDBSCAN_Clustering]]
- Rôle ML/DL dans l'architecture → [[16_Role_ML_DL_JeryMotroNet]]

---

*Dernière mise à jour : Mars 2026 — Version V2 (GEE Enrichissement)*
