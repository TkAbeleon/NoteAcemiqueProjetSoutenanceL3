# 🏷️ PROB-003 — Manque de Labels Terrain (Ground Truth)
#FireProject #Problem #Solution #Labelisation #Dataset #ML #DL
[[Glossaire_Tags]] | [[00_INDEX]]

---

## Métadonnées

| Champ | Valeur |
|-------|--------|
| **ID** | PROB-003 |
| **Date découverte** | 2026-02-23 |
| **Priorité** | 🔴 Haute |
| **Impact** | Précision des modèles DL limitée sans labels fiables |

---

## Description

Les modèles DL (U-Net, CNN) nécessitent des **masques de segmentation labellisés** :
- Pixel = forêt / sol nu / zone brûlée
- Idéalement vérifiés par des experts terrain à Madagascar

**Problème :** Aucune base de données de labels spécifique à Madagascar n'est disponible gratuitement. Créer des labels manuellement est très chronophage.

---

## Solutions

### Solution 1 — Labels Semi-Supervisés (PRIORITÉ)

Utiliser les **indices spectraux comme proxy de labels** :

```python
def auto_label_from_indices(ndvi, nbr, dnbr):
    """Labels automatiques basés sur seuils indices — approximation."""
    mask = np.zeros_like(ndvi)
    mask[ndvi > 0.4] = 0    # Forêt dense
    mask[ndvi < 0.2] = 1    # Sol nu / dégradé
    mask[dnbr > 0.1] = 2    # Zone brûlée (cicatrice feu)
    return mask
```

> **Limite :** Labels approximatifs → modèle apprend une version lissée de la réalité. Acceptable pour prototype de soutenance.

### Solution 2 — Transfer Learning (Poids Pré-entraînés)

Utiliser des modèles pré-entraînés sur des données africaines similaires :

- **DeepLabV3+** pré-entraîné sur Africa (ESA WorldCover)
- **Prithvi** : modèle IBM/NASA pré-entraîné sur Sentinel-2 mondial (open source)

```python
# Prithvi — modèle fondation NASA/IBM pour Sentinel-2
# https://huggingface.co/ibm-nasa-geospatial/Prithvi-100M
from transformers import AutoModelForSemanticSegmentation

model = AutoModelForSemanticSegmentation.from_pretrained(
    "ibm-nasa-geospatial/Prithvi-100M-sen1floods11"
)
# Fine-tuner sur les quelques labels disponibles pour Madagascar
```

### Solution 3 — Annotation Manuelle Ciblée

Annoter manuellement **50–100 patches** sur des zones connues :
- Utiliser **QGIS** + plugin de labellisation raster
- Zones prioritaires : Menabe, Analamanga, Boeny (zones à feux fréquents)
- **50–100 images bien labellisées > 1000 mal labellisées**

### Solution 4 — Validation avec Acteurs Terrain

Envoyer des cartes générées par le modèle à des acteurs locaux (ONG, gardes forestiers) pour validation qualitative.

---

## Impact sur le mémoire

> "La rareté des données labellisées spécifiques à Madagascar justifie l'utilisation du transfer learning et des labels semi-supervisés — une contrainte réelle qui renforce la pertinence du projet."

---

## Historique

| Date | Action | Tag |
|------|--------|-----|
| 2026-02-23 | Problème documenté | #Problem |
| — | Labels semi-supervisés à implémenter S3 | #Labelisation |
| — | Transfer Learning Prithvi à évaluer S6 | #DL |
