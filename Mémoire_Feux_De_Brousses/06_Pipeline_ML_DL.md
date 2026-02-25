# 🤖 Pipeline ML/DL — FireProject
#FireProject #ML #DL #Python #Classification #Prediction #TimeSeries
[[Glossaire_Tags]] | [[00_INDEX]]

---

## 1. VUE D'ENSEMBLE DU PIPELINE IA

```
DONNÉES FIRMS (CSV)          IMAGES SENTINEL-2 (GeoTIFF)
      ↓                              ↓
[FEATURES TABULAIRES]        [PATCHES 64×64 MULTI-BANDES]
      ↓                              ↓
┌─────────────┐              ┌──────────────────┐
│ ML Classique│              │  Deep Learning   │
│ RandomForest│              │  CNN / U-Net     │
│ XGBoost     │              │  ResNet (TL)     │
│ SVM         │              └──────────────────┘
└─────────────┘                      ↓
      ↓                       MASQUES SEGMENTATION
SCORES RISQUE (0–1)                  ↓
      ↓                    ┌──────────────────────┐
      └────────────────────►  LSTM (Séries temp.) │
                           │  Prédiction 48–72h   │
                           └──────────────────────┘
                                     ↓
                           ALERTES + RAPPORTS IA
```

---

## 2. MACHINE LEARNING (DONNÉES TABULAIRES FIRMS)

### 2.1 Features Engineering

```python
import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder

def create_features(df):
    """Crée toutes les features ML à partir des données FIRMS brutes."""

    # Features temporelles
    df['acq_datetime'] = pd.to_datetime(df['acq_date'] + ' ' + df['acq_time'].astype(str).str.zfill(4), format='%Y-%m-%d %H%M')
    df['month'] = df['acq_datetime'].dt.month
    df['hour'] = df['acq_datetime'].dt.hour
    df['dayofyear'] = df['acq_datetime'].dt.dayofyear
    df['is_dry_season'] = df['month'].isin([4, 5, 6, 7, 8, 9, 10]).astype(int)  # Saison sèche Madagascar

    # Features spatiales
    df['latitude_grid'] = (df['latitude'] * 10).round() / 10  # Grille 0.1°
    df['longitude_grid'] = (df['longitude'] * 10).round() / 10

    # Feature jour/nuit
    df['is_night'] = (df['daynight'] == 'N').astype(int)

    # Features thermiques normalisées
    df['frp_log'] = np.log1p(df['frp'])  # Log-transform (distribution très asymétrique)
    df['brightness_normalized'] = (df['brightness'] - 300) / 100  # Normalisation manuelle

    # Label : feu confirmé (semi-supervisé)
    # Confiance > 80% ET FRP > 10MW → feu certain
    # Confiance 30–80% → feu probable
    # Confiance < 30% → non-feu
    df['fire_label'] = 0
    df.loc[df['confidence'] >= 80, 'fire_label'] = 2  # Feu certain
    df.loc[(df['confidence'] >= 30) & (df['confidence'] < 80), 'fire_label'] = 1  # Probable

    return df

FEATURE_COLS = [
    'brightness', 'frp_log', 'bright_t31',
    'month', 'hour', 'dayofyear', 'is_dry_season',
    'is_night', 'latitude_grid', 'longitude_grid',
    'scan', 'track'
]
```

### 2.2 Random Forest — Classification

*Référence détaillée → [[TECH-001_Random_Forest]]*

```python
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import classification_report, roc_auc_score
import joblib

def train_random_forest(df, feature_cols, label_col='fire_label'):
    X = df[feature_cols].fillna(0)
    y = (df[label_col] >= 1).astype(int)  # Binaire : feu / non-feu

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.15, random_state=42, stratify=y
    )

    model = RandomForestClassifier(
        n_estimators=200,
        max_depth=15,
        min_samples_leaf=5,
        class_weight='balanced',  # Gérer déséquilibre feu/non-feu
        n_jobs=-1,
        random_state=42
    )

    model.fit(X_train, y_train)

    # Évaluation
    y_pred = model.predict(X_test)
    y_proba = model.predict_proba(X_test)[:, 1]

    print(classification_report(y_test, y_pred, target_names=['Non-feu', 'Feu']))
    print(f"AUC-ROC : {roc_auc_score(y_test, y_proba):.4f}")

    # Feature importance
    importances = pd.Series(model.feature_importances_, index=feature_cols)
    print("\nTop 5 features :")
    print(importances.nlargest(5))

    # Sauvegarde
    joblib.dump(model, "models_saved/rf_model.pkl")
    return model

def predict_risk_score(model, new_data, feature_cols):
    """Retourne score de risque (0–1) pour nouvelles détections."""
    X = new_data[feature_cols].fillna(0)
    return model.predict_proba(X)[:, 1]
```

### 2.3 XGBoost — Prédiction Zones à Risque

*Référence détaillée → [[TECH-002_XGBoost]]*

```python
import xgboost as xgb
from sklearn.metrics import mean_absolute_error

def train_xgboost_risk(df_temporal):
    """XGBoost pour prédire le risque dans les 48–72h suivantes."""

    # Features incluant historique 7 jours
    feature_cols = [
        'fire_count_7d',      # Nb feux 7 derniers jours dans la zone
        'frp_mean_7d',        # FRP moyen 7 derniers jours
        'ndvi_mean',          # NDVI moyen zone (végétation)
        'month', 'dayofyear',
        'is_dry_season',
        'precipitation_mm',   # Précipitations (si disponible)
    ]

    model = xgb.XGBClassifier(
        n_estimators=300,
        max_depth=6,
        learning_rate=0.05,
        subsample=0.8,
        colsample_bytree=0.8,
        scale_pos_weight=10,  # Déséquilibre classes
        random_state=42,
        use_label_encoder=False,
        eval_metric='auc'
    )

    # ...entraînement identique à RF...
    return model
```

---

## 3. DEEP LEARNING (IMAGES SENTINEL-2)

### 3.1 Préparation des données images

```python
import numpy as np
import rasterio
import torch
from torch.utils.data import Dataset, DataLoader

class FireDataset(Dataset):
    """Dataset PyTorch pour patches Sentinel-2."""

    def __init__(self, patches_dir, labels_dir, transform=None):
        self.patches = sorted(glob(f"{patches_dir}/*.npy"))
        self.labels = sorted(glob(f"{labels_dir}/*.npy"))
        self.transform = transform

    def __len__(self):
        return len(self.patches)

    def __getitem__(self, idx):
        # Charger patch multi-bandes (B04, B08, B11, B12)
        patch = np.load(self.patches[idx]).astype(np.float32)

        # Normalisation par bande (min-max)
        for i in range(patch.shape[0]):
            band_min, band_max = patch[i].min(), patch[i].max()
            if band_max > band_min:
                patch[i] = (patch[i] - band_min) / (band_max - band_min)

        label = np.load(self.labels[idx]).astype(np.long)

        return torch.tensor(patch), torch.tensor(label)
```

### 3.2 U-Net — Segmentation Zones Brûlées

*Référence détaillée → [[TECH-005_UNet]]*

```python
import torch
import torch.nn as nn

class DoubleConv(nn.Module):
    def __init__(self, in_ch, out_ch):
        super().__init__()
        self.conv = nn.Sequential(
            nn.Conv2d(in_ch, out_ch, 3, padding=1),
            nn.BatchNorm2d(out_ch),
            nn.ReLU(inplace=True),
            nn.Conv2d(out_ch, out_ch, 3, padding=1),
            nn.BatchNorm2d(out_ch),
            nn.ReLU(inplace=True)
        )
    def forward(self, x): return self.conv(x)

class UNet(nn.Module):
    def __init__(self, in_channels=4, num_classes=3):
        # in_channels=4 : B04, B08, B11, B12
        # num_classes=3 : forêt / sol nu / zone brûlée
        super().__init__()
        # Encodeur
        self.enc1 = DoubleConv(in_channels, 64)
        self.enc2 = DoubleConv(64, 128)
        self.enc3 = DoubleConv(128, 256)
        self.pool = nn.MaxPool2d(2)
        # Bottleneck
        self.bottleneck = DoubleConv(256, 512)
        # Décodeur avec skip connections
        self.up3 = nn.ConvTranspose2d(512, 256, 2, stride=2)
        self.dec3 = DoubleConv(512, 256)
        self.up2 = nn.ConvTranspose2d(256, 128, 2, stride=2)
        self.dec2 = DoubleConv(256, 128)
        self.up1 = nn.ConvTranspose2d(128, 64, 2, stride=2)
        self.dec1 = DoubleConv(128, 64)
        # Sortie
        self.final = nn.Conv2d(64, num_classes, 1)

    def forward(self, x):
        e1 = self.enc1(x)
        e2 = self.enc2(self.pool(e1))
        e3 = self.enc3(self.pool(e2))
        b  = self.bottleneck(self.pool(e3))
        d3 = self.dec3(torch.cat([self.up3(b), e3], dim=1))
        d2 = self.dec2(torch.cat([self.up2(d3), e2], dim=1))
        d1 = self.dec1(torch.cat([self.up1(d2), e1], dim=1))
        return self.final(d1)

def iou_score(pred_mask, true_mask, num_classes=3):
    """Calcul IoU par classe."""
    ious = []
    for cls in range(num_classes):
        intersection = ((pred_mask == cls) & (true_mask == cls)).sum().float()
        union = ((pred_mask == cls) | (true_mask == cls)).sum().float()
        if union == 0:
            ious.append(float('nan'))
        else:
            ious.append((intersection / union).item())
    return np.nanmean(ious)
```

### 3.3 LSTM — Prédiction Temporelle

*Référence détaillée → [[TECH-004_LSTM_TimeSeries]]*

```python
import torch.nn as nn

class FireLSTM(nn.Module):
    """LSTM pour prédire le risque feu dans les 48–72h."""

    def __init__(self, input_size=8, hidden_size=128, num_layers=2, output_size=1):
        # input_size=8 : nb feux, FRP moy, NDVI, temp, humidité, vent, mois, heure
        super().__init__()
        self.lstm = nn.LSTM(input_size, hidden_size, num_layers,
                           batch_first=True, dropout=0.3)
        self.fc = nn.Sequential(
            nn.Linear(hidden_size, 64),
            nn.ReLU(),
            nn.Dropout(0.2),
            nn.Linear(64, output_size),
            nn.Sigmoid()  # Probabilité de feu (0–1)
        )

    def forward(self, x):
        # x : (batch, seq_len=7, input_size)
        lstm_out, _ = self.lstm(x)
        return self.fc(lstm_out[:, -1, :])  # Prédiction sur dernier pas
```

---

## 4. MÉTRIQUES ET ÉVALUATION

### 4.1 Pour modèles ML (données tabulaires)

```python
from sklearn.metrics import (
    classification_report, roc_auc_score,
    confusion_matrix, f1_score
)

def evaluate_ml_model(model, X_test, y_test):
    y_pred = model.predict(X_test)
    y_proba = model.predict_proba(X_test)[:, 1]

    print("=== Rapport de Classification ===")
    print(classification_report(y_test, y_pred))
    print(f"AUC-ROC    : {roc_auc_score(y_test, y_proba):.4f}")
    print(f"F1 (feu)   : {f1_score(y_test, y_pred):.4f}")

    cm = confusion_matrix(y_test, y_pred)
    print(f"\nMatrice de confusion :\n{cm}")
    print(f"Faux négatifs (feux manqués) : {cm[1,0]} → CRITIQUE")
```

### 4.2 Pour modèles DL (images)

```python
def evaluate_dl_model(model, dataloader, device):
    model.eval()
    total_iou = 0
    n_batches = 0

    with torch.no_grad():
        for images, masks in dataloader:
            images, masks = images.to(device), masks.to(device)
            outputs = model(images)
            pred_masks = outputs.argmax(dim=1)
            total_iou += iou_score(pred_masks.cpu(), masks.cpu())
            n_batches += 1

    mean_iou = total_iou / n_batches
    print(f"IoU moyen : {mean_iou:.4f} (objectif : ≥ 0.70)")
    return mean_iou
```

---

## 5. GUIDE D'ENTRAÎNEMENT SUR GOOGLE COLAB

```python
# Colab : activer GPU → Exécution > Modifier le type d'exécution > GPU T4

# Vérification GPU
import torch
print(f"GPU disponible : {torch.cuda.is_available()}")
print(f"Nom GPU : {torch.cuda.get_device_name(0)}")

# Entraînement U-Net
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = UNet(in_channels=4, num_classes=3).to(device)
optimizer = torch.optim.Adam(model.parameters(), lr=1e-3)
criterion = nn.CrossEntropyLoss(weight=torch.tensor([1.0, 2.0, 5.0]).to(device))
# Poids plus élevé pour zones brûlées (classe rare)

scheduler = torch.optim.lr_scheduler.ReduceLROnPlateau(optimizer, patience=5)

for epoch in range(50):
    model.train()
    epoch_loss = 0
    for images, masks in train_loader:
        images, masks = images.to(device), masks.to(device)
        optimizer.zero_grad()
        outputs = model(images)
        loss = criterion(outputs, masks)
        loss.backward()
        optimizer.step()
        epoch_loss += loss.item()

    val_iou = evaluate_dl_model(model, val_loader, device)
    scheduler.step(1 - val_iou)
    print(f"Epoch {epoch+1}/50 | Loss: {epoch_loss/len(train_loader):.4f} | Val IoU: {val_iou:.4f}")

# Sauvegarder
torch.save(model.state_dict(), "unet_fireproject.pth")
```

---

*Architecture → [[04_Architecture_Globale]]*
*Techniques détaillées → [[TECH-001_Random_Forest]] | [[TECH-005_UNet]] | [[TECH-004_LSTM_TimeSeries]]*
