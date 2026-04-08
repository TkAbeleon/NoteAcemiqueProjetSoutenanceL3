# 🧠 TECH-003 — CNN Classification
#FireProject #DL #Classification #Python #Notebook
[[Glossaire_Tags]] | [[06_Pipeline_ML_DL]] | [[00_INDEX]]

---

| Champ | Valeur |
|-------|--------|
| **Nom** | Convolutional Neural Network (CNN) |
| **Type** | Deep Learning — Vision |
| **Phase** | Phase 2 (Semaine 6) |
| **Entrée** | Patches Sentinel-2 (64×64×4 bandes) |
| **Sortie** | Classe (forêt / sol nu / zone brûlée) |

---

## Architecture CNN Baseline

```
Input: (batch, 4, 64, 64)   ← 4 bandes : B04, B08, B11, B12
Conv2D(4→32, k=3) + BN + ReLU + MaxPool(2)
Conv2D(32→64, k=3) + BN + ReLU + MaxPool(2)
Conv2D(64→128, k=3) + BN + ReLU + MaxPool(2)
Flatten → Dense(256) + Dropout(0.4)
Dense(3) + Softmax    ← 3 classes
```

---

## Transfer Learning — ResNet-18

Utiliser ResNet-18 pré-entraîné sur ImageNet → adapter la dernière couche.

```python
import torchvision.models as models

resnet = models.resnet18(pretrained=True)

# Adapter première couche pour 4 bandes (ImageNet = 3 bandes RGB)
resnet.conv1 = nn.Conv2d(4, 64, kernel_size=7, stride=2, padding=3, bias=False)

# Adapter dernière couche
resnet.fc = nn.Linear(512, 3)  # 3 classes
```

**Avantage Transfer Learning :** Même avec peu de données labellisées pour Madagascar, les features de bas niveau (bords, textures) appris sur ImageNet restent utiles.

---

## Métriques cibles

| Métrique | Cible |
|----------|-------|
| Accuracy globale | ≥ 85% |
| F1 (zones brûlées) | ≥ 0.80 |

---

## Notes

- Entraîner sur **Google Colab GPU T4** (gratuit)
- Augmentation données : flip horizontal/vertical, rotation 90°
- Sauvegarder poids : `cnn_model.pth`
