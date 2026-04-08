# ☁️ PROB-002 — Couverture Nuageuse
#FireProject #Problem #Solution #Risque #Sentinel2 #Dataset
[[Glossaire_Tags]] | [[00_INDEX]]

---

## Métadonnées

| Champ | Valeur |
|-------|--------|
| **ID** | PROB-002 |
| **Date découverte** | 2026-02-23 |
| **Priorité** | 🔴 Haute (saison des pluies) |
| **Statut** | ✅ Solution identifiée (Sentinel-1 SAR) |

---

## Description

Madagascar a deux saisons marquées :
- **Saison des pluies (Nov–Mar)** : couverture nuageuse 60–90% → Sentinel-2 optique inutilisable
- **Saison sèche (Avr–Oct)** : couverture nuageuse < 30% → Sentinel-2 optimal

**Impact :** En saison des pluies, impossible d'obtenir des images optiques propres pour le DL (U-Net, CNN).

---

## Solutions

### Solution 1 — Sentinel-1 SAR (Radar) ✅

Le radar **pénètre les nuages** et fonctionne la nuit.

```python
# Télécharger Sentinel-1 SAR (polarisation VV + VH)
# Résolution 10m — même que Sentinel-2
# Format : GeoTIFF dB (décibels)

# Indices SAR utiles pour feux :
# - Variation de rétrodiffusion VV avant/après feu
# - Ratio VH/VV (sensible à la structure de végétation)
```

### Solution 2 — Mosaïques Temporelles

Créer une image composite en prenant la médiane de plusieurs images sur 30 jours → élimine les nuages ponctuels.

```python
import numpy as np

def cloud_free_median(images_list):
    """
    Calcule la médiane pixel par pixel sur N images.
    Les nuages (valeurs aberrantes) sont automatiquement exclus.
    """
    stack = np.stack(images_list, axis=0)
    return np.nanmedian(stack, axis=0)
```

### Solution 3 — Stratégie Saisonnière

| Saison | Approche principale |
|--------|--------------------| 
| Sèche (Avr–Oct) | Sentinel-2 optique + U-Net |
| Pluies (Nov–Mar) | Sentinel-1 SAR + ML tabulaire FIRMS |

---

## Notes

- Sentinel-1 SAR disponible gratuitement via Copernicus (même compte)
- Adapter U-Net pour SAR : changer `in_channels=4` → `in_channels=2` (VV, VH)
- Priorité : implémenter en Phase 2 si temps disponible

---

## Historique

| Date | Action | Tag |
|------|--------|-----|
| 2026-02-23 | Problème documenté | #Problem |
| — | Solution SAR à implémenter S8+ | #Avancement |
