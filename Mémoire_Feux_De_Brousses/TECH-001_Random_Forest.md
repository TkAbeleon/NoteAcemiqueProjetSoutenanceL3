# 🌲 TECH-001 — Random Forest
#FireProject #ML #Classification #Prediction #Python
[[Glossaire_Tags]] | [[06_Pipeline_ML_DL]] | [[00_INDEX]]

---

## Métadonnées

| Champ | Valeur |
|-------|--------|
| **Nom** | Random Forest Classifier |
| **Type** | Machine Learning — Ensemble |
| **Phase projet** | Phase 1 (Semaine 4) |
| **Priorité** | 🔴 Critique — Modèle principal |

---

## Description

Random Forest = ensemble de **N arbres de décision** entraînés sur des sous-ensembles aléatoires des données. La prédiction finale = vote majoritaire des arbres.

**Pourquoi Random Forest pour FireProject ?**
- Robuste aux données manquantes (FIRMS a parfois des NaN)
- Interprétable (feature importance → expliquer au jury)
- Pas besoin de normalisation des features
- Gère bien le déséquilibre feu/non-feu avec `class_weight='balanced'`
- Rapide à entraîner même sur PC modeste

---

## Hyperparamètres choisis

| Paramètre | Valeur | Justification |
|-----------|--------|---------------|
| `n_estimators` | 200 | Compromis précision/temps |
| `max_depth` | 15 | Éviter sur-apprentissage |
| `min_samples_leaf` | 5 | Généralisation |
| `class_weight` | `balanced` | Compenser rareté des feux |
| `n_jobs` | -1 | Utiliser tous les CPU |

---

## Résultats attendus

| Métrique | Minimum | Cible |
|----------|---------|-------|
| Accuracy | 80% | 88% |
| F1-Score (feu) | 0.78 | 0.85 |
| AUC-ROC | 0.82 | 0.90 |
| Faux négatifs (feux manqués) | < 15% | < 8% |

> ⚠️ **PRIORITÉ** : Minimiser les faux négatifs (feux non détectés) même au prix de plus de faux positifs.

---

## Usage dans le projet

1. **Inférence quotidienne** : score de risque pour chaque détection FIRMS
2. **Seuil d'alerte** : score > 0.70 → alerte générée
3. **Explication au jury** : feature importance montre quelles variables comptent

---

## Commande d'entraînement

```bash
python scripts/models/rf_classifier.py \
  --input data/processed/firms_clean.csv \
  --output models_saved/rf_model.pkl \
  --threshold 0.70
```

---

## Notes

- Réentraîner mensuellemement avec nouvelles données
- Comparer avec XGBoost → [[TECH-002_XGBoost]]
- Le modèle `.pkl` est appelé directement par n8n → [[07_Automatisation_n8n]]
