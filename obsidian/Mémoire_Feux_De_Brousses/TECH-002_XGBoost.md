# ⚡ TECH-002 — XGBoost
#FireProject #ML #Prediction #TimeSeries #Python
[[Glossaire_Tags]] | [[06_Pipeline_ML_DL]] | [[00_INDEX]]

---

| Champ | Valeur |
|-------|--------|
| **Nom** | XGBoost Classifier (eXtreme Gradient Boosting) |
| **Type** | ML — Gradient Boosting |
| **Phase** | Phase 2 (Semaine 8) |
| **Usage** | Prédiction zones à risque 48–72h |

---

## Description

XGBoost = gradient boosting optimisé. Chaque arbre corrige les erreurs du précédent. Généralement plus précis que Random Forest sur données tabulaires structurées.

**Avantage clé pour FireProject :** Intègre l'**historique temporel** (7 jours glissants) pour prédire le risque futur — pas juste classifier l'existant.

---

## Features spécifiques XGBoost

| Feature | Calcul | Intérêt |
|---------|--------|---------|
| `fire_count_7d` | Nb détections zone (7j) | Tendance récente |
| `frp_mean_7d` | FRP moyen (7j) | Intensité tendance |
| `fire_streak_days` | Jours consécutifs avec feux | Persistance |
| `ndvi_delta` | Variation NDVI (14j) | Stress végétation |

---

## Hyperparamètres

```python
xgb.XGBClassifier(
    n_estimators=300,
    max_depth=6,
    learning_rate=0.05,      # Petit pour généralisation
    subsample=0.8,
    colsample_bytree=0.8,
    scale_pos_weight=10,     # Déséquilibre classes feux
    eval_metric='auc',
    early_stopping_rounds=20
)
```

---

## Résultats attendus

| Métrique | Cible |
|----------|-------|
| AUC-ROC prédiction 48h | ≥ 0.85 |
| Précision (score > 0.7) | ≥ 75% |

---

## Notes

- Comparer directement avec RF → tableau dans mémoire
- Si AUC-ROC XGBoost > RF : utiliser XGBoost comme modèle principal
