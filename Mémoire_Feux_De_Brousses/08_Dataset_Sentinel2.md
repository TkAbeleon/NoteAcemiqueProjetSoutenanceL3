# 🛰️ Dataset — Sentinel-2 ESA
#FireProject #Dataset #Sentinel2 #DataCleaning #Satellite #DL
[[Glossaire_Tags]] | [[05_APIs_et_Donnees]] | [[00_INDEX]]

---

## Métadonnées

| Champ | Valeur |
|-------|--------|
| **Nom** | Sentinel-2 L2A — Madagascar |
| **Source** | ESA Copernicus |
| **Capteur** | MSI (Multispectral Instrument) |
| **Résolution** | 10m (B02,B03,B04,B08) / 20m (B11,B12) |
| **Zone** | Madagascar |
| **Revisite** | ~5 jours (S2A + S2B combinés) |
| **Format** | GeoTIFF ou JP2 |
| **Coût** | Gratuit (compte Copernicus) |

---

## Bandes Utilisées pour FireProject

| Bande | Longueur d'onde | Résolution | Usage |
|-------|-----------------|------------|-------|
| B04 (Rouge) | 665nm | 10m | NDVI, couleur naturelle |
| B08 (PIR) | 842nm | 10m | NDVI, végétation |
| B11 (SWIR1) | 1610nm | 20m | NBR, zones brûlées |
| B12 (SWIR2) | 2190nm | 20m | NBR, minéraux |
| B02 (Bleu) | 490nm | 10m | Visualisation RGB |

---

## Indices Calculés

```python
import numpy as np

def compute_all_indices(b02, b04, b08, b11, b12):
    """Calcule tous les indices spectraux utiles FireProject."""

    # Éviter division par zéro
    eps = 1e-10

    # NDVI : Normalized Difference Vegetation Index
    # Forêt dense → proche de 1 | Sol nu → proche de 0 | Eau → négatif
    ndvi = (b08 - b04) / (b08 + b04 + eps)

    # NBR : Normalized Burn Ratio
    # Zone saine → positif | Zone brûlée → très négatif
    nbr = (b08 - b12) / (b08 + b12 + eps)

    # dNBR : Différentiel NBR (avant - après feu)
    # Nécessite deux images temporelles de la même zone
    # dNBR > 0.27 : brûlage sévère
    # dNBR 0.10–0.27 : brûlage modéré
    # dNBR < 0.10 : brûlage faible / non brûlé

    # EVI : Enhanced Vegetation Index (moins sensible à l'atmosphère)
    evi = 2.5 * (b08 - b04) / (b08 + 6*b04 - 7.5*b02 + 1 + eps)

    return {
        'ndvi': np.clip(ndvi, -1, 1),
        'nbr': np.clip(nbr, -1, 1),
        'evi': np.clip(evi, -1, 1)
    }
```

---

## Notes de Prétraitement

- Rééchantillonner B11, B12 de 20m → 10m pour cohérence
- Appliquer masque nuages (bande SCL disponible dans L2A)
- Normaliser par bande avant entraînement DL
- Taille patches recommandée : 64×64 pixels = 640m × 640m terrain

---

## Zones Prioritaires à Télécharger

| Zone | Justification |
|------|---------------|
| Menabe (ouest) | Zone la plus touchée par les feux |
| Boeny (nord-ouest) | Déforestation active |
| Analamanga (centre) | Feux récurrents, validation possible |
| Alaotra (nord-est) | Brûlis agricoles |

---

## Liens croisés

- PROB-002 (nuages) → [[PROB-002_Couverture_nuageuse]]
- TECH-005 U-Net → [[TECH-005_UNet]]
- TECH-003 CNN → [[TECH-003_CNN_Segmentation]]
