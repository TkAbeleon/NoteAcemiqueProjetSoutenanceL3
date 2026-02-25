# 🤖 JeryMotroNet — Modèle Original
#JeryMotro #MemoireL3 #ML #DL #Classification #Prediction
[[Glossaire_Tags]] | [[00_INDEX]] | [[01_Cahier_des_Charges]]

---

> **JeryMotroNet = Modèle ML/DL original entraîné sur données malgaches.**
> Contribution académique centrale du mémoire L3.
> Deux branches : XGBoost (classification) + ConvLSTM (prédiction spatiale J+1)

---

## 1. ARCHITECTURE GLOBALE MADFIRENET

```
Données enrichies (FIRMS + ERA5 + features)
           ↓
    ┌──────┴──────┐
    ▼             ▼
[Branche A]   [Branche B]
XGBoost       ConvLSTM
    │               │
Classification   Prédiction
risque (0/1)     carte J+1
+ score (0–1)    (grille 375m)
    │               │
    └──────┬─────────┘
           ▼
    Résultats JSON → FastAPI → Frontend
```

---

## 2. BRANCHE A — XGBoost Classification

*Référence complète → [[04_JeryMotroNet_XGBoost]]*

**Tâche :** Classifier chaque détection FIRMS en `feu_réel` (1) ou `bruit_thermique/non_feu` (0)
**Innovation :** Combiner les features FIRMS + ERA5 + cluster_features pour dépasser la simple confiance NASA

### Features d'entrée

| Feature | Calcul | Source |
|---------|--------|--------|
| `diff_brightness` | `brightness - bright_t31` | FIRMS — **Feature clé** |
| `frp_log` | `log1p(frp)` | FIRMS |
| `local_hour` | `acq_time UTC + 3` | FIRMS |
| `is_dry_season` | `mois ∈ [4–10]` | FIRMS |
| `daynight_bin` | `D=1, N=0` | FIRMS |
| `cluster_size` | Nb points dans le cluster | HDBSCAN |
| `cluster_frp_total` | Somme FRP du cluster | HDBSCAN |
| `temperature_2m` | Température air (°C) | ERA5 / GEE |
| `relative_humidity` | Humidité relative (%) | ERA5 / GEE |
| `wind_speed_10m` | Vitesse vent (m/s) | ERA5 / GEE |
| `region_encoded` | Région administrative (LabelEncoded) | GeoAdmin |

### Hyperparamètres XGBoost

```python
import xgboost as xgb

model = xgb.XGBClassifier(
    n_estimators=500,
    max_depth=7,
    learning_rate=0.03,
    subsample=0.8,
    colsample_bytree=0.8,
    min_child_weight=5,
    scale_pos_weight=15,      # Déséquilibre fort feu/non-feu
    eval_metric=['auc', 'logloss'],
    early_stopping_rounds=30,
    random_state=42,
    n_jobs=-1
)
```

### Label Semi-Supervisé

```python
def create_fire_label(df):
    """
    Label basé sur confiance + FRP.
    Semi-supervisé car pas de ground truth terrain Madagascar.
    """
    df['fire_label'] = 0

    # Feu certain : VIIRS high + FRP > 15MW
    df.loc[(df['confidence'] == 'high') & (df['frp'] > 15), 'fire_label'] = 1

    # Feu probable : VIIRS nominal + FRP > 10MW + saison sèche
    df.loc[
        (df['confidence'] == 'nominal') &
        (df['frp'] > 10) &
        (df['is_dry_season'] == 1),
        'fire_label'
    ] = 1

    # MODIS : confiance numérique ≥ 70 + FRP > 10MW
    df.loc[
        (df['source'] == 'MODIS') &
        (df['confidence'] >= 70) &
        (df['frp'] > 10),
        'fire_label'
    ] = 1

    return df
```

### Métriques Cibles XGBoost

| Métrique | Cible | Justification |
|----------|-------|---------------|
| Recall (feux) | ≥ +25% vs NASA brut | **Objectif central** — moins de feux manqués |
| Précision (feux) | ≥ 75% | Éviter trop de fausses alertes |
| AUC-ROC | ≥ 0.88 | Qualité globale |
| F1-Score | ≥ 0.80 | Équilibre précision/rappel |

---

## 3. BRANCHE B — ConvLSTM Prédiction J+1

*Référence complète → [[05_JeryMotroNet_ConvLSTM]]*

**Tâche :** Prédire la carte de risque incendie pour J+1 sur une grille couvrant Madagascar
**Innovation :** Utiliser la dimension spatio-temporelle des données FIRMS (séquences sur grille)

### Principe ConvLSTM

```
ConvLSTM = LSTM + Convolution spatiale
→ Capture à la fois les patterns temporels (7 jours) ET spatiaux (voisinage)
→ Parfait pour des données grille (cartes) évoluant dans le temps
```

### Construction de la Grille Madagascar

```python
import numpy as np
import geopandas as gpd
from shapely.geometry import box

def create_madagascar_grid(resolution_m=375):
    """Crée une grille régulière sur Madagascar à 375m (résolution VIIRS)."""

    # Bbox Madagascar
    west, south, east, north = 43.0, -25.5, 50.5, -11.5

    # Conversion degrés → mètres approximatif (1° ≈ 111km)
    deg_per_pixel = resolution_m / 111000

    lons = np.arange(west, east, deg_per_pixel)
    lats = np.arange(south, north, deg_per_pixel)

    grid_width = len(lons)   # ~1978 colonnes
    grid_height = len(lats)  # ~1556 lignes

    return lons, lats, grid_width, grid_height  # Grille ~1978×1556

# Taille finale : trop grande pour ConvLSTM complet
# → Diviser en patches 64×64 ou travailler sur grille dégradée (1km)
GRID_SIZE = 64  # Patches 64×64 pixels pour l'entraînement
```

### Architecture ConvLSTM

```python
import torch
import torch.nn as nn

class ConvLSTMCell(nn.Module):
    def __init__(self, in_channels, hidden_channels, kernel_size=3):
        super().__init__()
        padding = kernel_size // 2
        self.conv = nn.Conv2d(
            in_channels + hidden_channels,
            4 * hidden_channels,   # i, f, o, g gates
            kernel_size, padding=padding
        )
        self.hidden_channels = hidden_channels

    def forward(self, x, h_prev, c_prev):
        combined = torch.cat([x, h_prev], dim=1)
        gates = self.conv(combined)
        i, f, o, g = gates.chunk(4, dim=1)
        i, f, o = torch.sigmoid(i), torch.sigmoid(f), torch.sigmoid(o)
        g = torch.tanh(g)
        c = f * c_prev + i * g
        h = o * torch.tanh(c)
        return h, c

class JeryMotroConvLSTM(nn.Module):
    """
    Prend 7 jours de cartes FRP + features → prédit carte risque J+1
    """
    def __init__(self, in_channels=5, hidden_channels=32):
        # in_channels = 5 : frp_grid, brightness_grid, ndvi_proxy,
        #                    temperature, is_dry_season
        super().__init__()
        self.convlstm1 = ConvLSTMCell(in_channels, hidden_channels)
        self.convlstm2 = ConvLSTMCell(hidden_channels, hidden_channels)
        self.output_conv = nn.Conv2d(hidden_channels, 1, kernel_size=1)
        self.sigmoid = nn.Sigmoid()
        self.hidden_channels = hidden_channels

    def forward(self, x):
        # x : (batch, seq_len=7, channels=5, H=64, W=64)
        batch, seq_len, C, H, W = x.shape
        device = x.device

        h1 = torch.zeros(batch, self.hidden_channels, H, W, device=device)
        c1 = torch.zeros_like(h1)
        h2 = torch.zeros_like(h1)
        c2 = torch.zeros_like(h1)

        for t in range(seq_len):
            h1, c1 = self.convlstm1(x[:, t], h1, c1)
            h2, c2 = self.convlstm2(h1, h2, c2)

        # Prédiction J+1 : carte probabilité feu 64×64
        out = self.sigmoid(self.output_conv(h2))
        return out  # (batch, 1, 64, 64)
```

### Métriques Cibles ConvLSTM

| Métrique | Cible |
|----------|-------|
| MAE carte J+1 | < 0.15 (erreur absolue moyenne prob) |
| Précision zones à risque > 0.7 | ≥ 70% |
| Recall zones effectivement brûlées J+1 | ≥ 65% |

---

## 4. INFÉRENCE UNIFIÉE

```python
# ml/inference/run_madfirenet.py
import joblib, torch, json
import pandas as pd

class JeryMotroNetInference:
    def __init__(self, xgb_path, convlstm_path):
        self.xgb_model = joblib.load(xgb_path)
        self.convlstm = torch.load(convlstm_path, map_location='cpu')
        self.convlstm.eval()

    def predict_points(self, df: pd.DataFrame) -> pd.DataFrame:
        """XGBoost : score risque pour chaque point."""
        X = df[FEATURE_COLS].fillna(0)
        df['risk_score'] = self.xgb_model.predict_proba(X)[:, 1]
        df['fire_predicted'] = (df['risk_score'] > 0.70).astype(int)
        return df

    def predict_risk_map(self, sequence: torch.Tensor) -> dict:
        """ConvLSTM : carte risque J+1."""
        with torch.no_grad():
            risk_map = self.convlstm(sequence.unsqueeze(0))
        return risk_map.squeeze().numpy().tolist()  # → JSON pour FastAPI
```

---

*Clustering → [[05_HDBSCAN_Clustering]]*
*Feature Engineering → [[06_Feature_Engineering]]*
*FastAPI → [[09_FastAPI_Backend]]*
