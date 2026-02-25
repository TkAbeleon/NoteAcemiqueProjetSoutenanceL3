# 🛠️ PROB-003 — GPU Insuffisant pour DL
#JeryMotro #Problem #Solution #DL #Notebook
[[Glossaire_Tags]] | [[00_INDEX]]

| Champ | Valeur |
|-------|--------|
| **ID** | PROB-003 |
| **Priorité** | 🟠 Moyenne |
| **Statut** | ✅ Solution = Google Colab T4 |

## Description
Le ConvLSTM nécessite un GPU pour l'entraînement. Un PC standard sans GPU dédié prend des heures pour une seule epoch.

## Solutions

**Solution 1 (priorité) — Google Colab GPU T4** : Gratuit, ~4–6h GPU/jour → suffisant pour entraîner ConvLSTM en ~50 epochs sur patches 64×64.

**Solution 2 — Modèle plus léger** : Si ConvLSTM trop lourd → utiliser LSTM simple (1D) sur séries temporelles de features agrégées par région. Moins précis géographiquement mais fonctionnel.

**Solution 3 — Transfer Learning** : Utiliser Prithvi (IBM/NASA) pré-entraîné sur Sentinel-2 → fine-tuning léger possible sur CPU.

## Commande Colab

```python
# Vérifier GPU disponible
import torch
print(f"GPU : {torch.cuda.get_device_name(0)}")
# → Tesla T4 (16GB VRAM) — suffisant pour ConvLSTM 64×64

# Monter Google Drive pour persister les modèles
from google.colab import drive
drive.mount('/content/drive')
```

| Date | Action |
|------|--------|
| 2026-02-23 | Documenté |
