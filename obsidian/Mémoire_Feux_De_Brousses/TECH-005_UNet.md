# 🗺️ TECH-005 — U-Net Segmentation
#FireProject #DL #Classification #Python #Notebook
[[Glossaire_Tags]] | [[06_Pipeline_ML_DL]] | [[00_INDEX]]

---

| Champ | Valeur |
|-------|--------|
| **Nom** | U-Net (Architecture encodeur-décodeur) |
| **Type** | Deep Learning — Segmentation sémantique |
| **Phase** | Phase 2 (Semaine 7) |
| **Entrée** | Images Sentinel-2 (64×64×4 bandes) |
| **Sortie** | Masque segmentation pixel par pixel |
| **Classes** | 3 : forêt (0) / sol nu (1) / zone brûlée (2) |

---

## Pourquoi U-Net ?

U-Net est l'architecture de référence pour la **segmentation d'images satellitaires** :
- Développée initialement pour la bio-médicale (2015) → très adaptée aux images à faible résolution
- **Skip connections** : préserve les détails fins (contours des zones brûlées)
- Fonctionne bien avec **peu de données labellisées** (essentiel pour Madagascar)

---

## Architecture U-Net (simplifiée pour FireProject)

```
ENCODEUR (compression)          DÉCODEUR (reconstruction)
Input (4,64,64)
│
DoubleConv → 64 ──────────────────────→ Concat → DoubleConv → 64
│                                                              │
MaxPool                                              ConvTranspose
│                                                              │
DoubleConv → 128 ─────────────────→ Concat → DoubleConv → 128
│                                                              │
MaxPool                                              ConvTranspose
│                                                              │
DoubleConv → 256 ─────────────→ Concat → DoubleConv → 256
│                                                              │
MaxPool                                              ConvTranspose
│                                                              │
BOTTLENECK: DoubleConv(256→512)                               │
                                                              │
Output: Conv2d(64→3) = masque (3 classes, 64×64)
```

---

## Création des masques (labels)

```python
import numpy as np

def create_segmentation_mask(ndvi, nbr, dnbr):
    """
    Crée masque segmentation basé sur indices spectraux.
    """
    mask = np.zeros_like(ndvi, dtype=np.int64)

    # Forêt : NDVI > 0.4
    mask[ndvi > 0.4] = 0

    # Sol nu / dégradé : NDVI < 0.2
    mask[ndvi < 0.2] = 1

    # Zone brûlée : dNBR > 0.1 (cicatrice de feu)
    mask[dnbr > 0.1] = 2

    return mask
```

> ⚠️ Ces seuils sont des **valeurs de départ** — à calibrer sur des zones connues de Madagascar.

---

## Fonction de perte

```python
# Weighted Cross Entropy : classe "zone brûlée" très rare
criterion = nn.CrossEntropyLoss(
    weight=torch.tensor([1.0, 1.5, 5.0])  # Poids plus élevé pour zones brûlées
)

# Alternative : Dice Loss (mieux pour segmentation déséquilibrée)
def dice_loss(pred, target, num_classes=3):
    loss = 0
    for cls in range(num_classes):
        pred_cls = (pred == cls).float()
        target_cls = (target == cls).float()
        intersection = (pred_cls * target_cls).sum()
        loss += 1 - (2 * intersection + 1) / (pred_cls.sum() + target_cls.sum() + 1)
    return loss / num_classes
```

---

## Métriques cibles

| Métrique | Minimum | Cible |
|----------|---------|-------|
| IoU global | 0.65 | 0.75 |
| IoU (zone brûlée) | 0.60 | 0.70 |
| Dice Score global | 0.70 | 0.80 |

---

## Notes

- Entraîner sur Colab GPU — ~2–3h pour 50 epochs
- Augmentation : flip + rotation + bruit gaussien
- Sauvegarder les poids du meilleur epoch (IoU validation max)
- Intégrer dans workflow Sentinel-2 → [[07_Automatisation_n8n]]
