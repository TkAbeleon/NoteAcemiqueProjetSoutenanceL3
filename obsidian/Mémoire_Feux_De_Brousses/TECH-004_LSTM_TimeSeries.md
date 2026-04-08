# ⏱️ TECH-004 — LSTM Séries Temporelles
#FireProject #DL #TimeSeries #Prediction #Python
[[Glossaire_Tags]] | [[06_Pipeline_ML_DL]] | [[00_INDEX]]

---

| Champ | Valeur |
|-------|--------|
| **Nom** | Long Short-Term Memory (LSTM) |
| **Type** | Deep Learning — Séries temporelles |
| **Phase** | Phase 3 (Semaine 9) |
| **Entrée** | Séquences 7 jours × 8 variables |
| **Sortie** | Probabilité feu 48–72h (0–1) |

---

## Pourquoi LSTM pour les feux ?

Les feux de brousse suivent des **patterns temporels** :
- Accumulation de jours secs → risque croissant
- Séquence de chaleur + vent fort → précurseurs
- Historique zone → certaines régions récurrentes

Le LSTM capture ces **dépendances à long terme** que RF/XGBoost voient partiellement.

---

## Features d'entrée (par pas de temps)

| Feature | Source | Normalisation |
|---------|--------|---------------|
| `fire_count` | FIRMS | Min-max |
| `frp_mean` | FIRMS | Log + min-max |
| `ndvi_mean` | Sentinel-2 | Min-max |
| `temperature_max` | (météo si dispo) | Z-score |
| `humidity_min` | (météo si dispo) | Z-score |
| `wind_speed` | (météo si dispo) | Min-max |
| `month_sin` | Encodage circulaire | Déjà normalisé |
| `month_cos` | Encodage circulaire | Déjà normalisé |

> ⚠️ Si données météo indisponibles : utiliser uniquement features FIRMS + NDVI (5 features au lieu de 8)

---

## Architecture

```
Input: (batch, seq_len=7, features=8)
LSTM(8→128, layers=2, dropout=0.3)
    → prend les 7 derniers jours
    → retient patterns importants
Dense(128→64) + ReLU + Dropout(0.2)
Dense(64→1) + Sigmoid
Output: probabilité feu 48h (0–1)
```

---

## Métriques cibles

| Métrique | Cible |
|----------|-------|
| AUC-ROC (prédiction 48h) | ≥ 0.82 |
| Précision (si score > 0.7) | ≥ 70% |
| Rappel (vrais risques détectés) | ≥ 80% |

---

## Notes

- Données météo : utiliser ERA5 (gratuit via Google Earth Engine) si besoin
- Fenêtre temporelle : tester 7j vs 14j vs 30j
- Intégrer dans n8n workflow `ml_inference` après RF
