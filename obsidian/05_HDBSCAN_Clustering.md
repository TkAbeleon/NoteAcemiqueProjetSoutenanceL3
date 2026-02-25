# 🔵 HDBSCAN Clustering — JeryMotro Platform
#JeryMotro #MemoireL3 #ML #Clustering #Python
[[Glossaire_Tags]] | [[00_INDEX]] | [[04_JeryMotroNet]]

---

## Pourquoi HDBSCAN pour les feux de brousse ?

Les feux de brousse ne se distribuent pas uniformément — ils forment des **clusters naturels** (zones contiguës brûlant en même temps). HDBSCAN est idéal car :

- **Pas besoin de définir le nombre de clusters** à l'avance (≠ K-Means)
- **Gère le bruit** (points isolés = fausses détections)
- **Fonctionne sur données spatiales et temporelles** simultanément

---

## Paramètres retenus

| Paramètre | Valeur | Justification |
|-----------|--------|---------------|
| `min_cluster_size` | 3 | Au moins 3 points FIRMS pour former un feu |
| Rayon spatial | 750m | Résolution VIIRS = 375m → 2× pour zone adjacente |
| Fenêtre temporelle | 48h | Un feu de brousse dure rarement plus de 48h sans extension |
| `min_samples` | 2 | Sensibilité raisonnable (pas trop de bruit) |
| Métrique | `haversine` | Distance correcte sur sphère terrestre |

---

## Implémentation

```python
# ml/clustering/hdbscan_cluster.py
import numpy as np
import pandas as pd
import hdbscan
from sklearn.preprocessing import StandardScaler

def cluster_fire_points(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clustering spatio-temporel HDBSCAN des points FIRMS.
    Combine distance spatiale (km) + distance temporelle (heures).
    """
    if len(df) < 3:
        df['cluster_id'] = -1
        return df

    # Coordonnées en radians pour haversine
    coords_rad = np.radians(df[['latitude', 'longitude']].values)

    # Normaliser le temps (heures depuis premier point)
    df['time_hours'] = (
        pd.to_datetime(df['acq_date'] + ' ' + df['acq_time'].astype(str).str.zfill(4))
        - pd.to_datetime(df['acq_date'].min())
    ).dt.total_seconds() / 3600

    # Distance temporelle normalisée pour être comparable (750m ≈ 48h)
    # 750m sur Terre ≈ 750/6371000 ≈ 0.0001178 radians
    time_normalized = df['time_hours'].values / 48 * 0.0001178
    time_normalized = time_normalized.reshape(-1, 1)

    # Features : (lat_rad, lon_rad, time_normalized)
    features = np.hstack([coords_rad, time_normalized])

    clusterer = hdbscan.HDBSCAN(
        min_cluster_size=3,
        min_samples=2,
        metric='euclidean',   # sur features déjà en radians
        cluster_selection_epsilon=0.0001178,  # ~750m en radians
        prediction_data=True
    )
    df['cluster_id'] = clusterer.fit_predict(features)

    # Calculer features des clusters
    cluster_stats = df[df['cluster_id'] != -1].groupby('cluster_id').agg(
        cluster_size=('frp', 'count'),
        cluster_frp_total=('frp', 'sum'),
        cluster_frp_max=('frp', 'max'),
        cluster_brightness_mean=('brightness', 'mean'),
        cluster_center_lat=('latitude', 'mean'),
        cluster_center_lon=('longitude', 'mean'),
    ).reset_index()

    df = df.merge(cluster_stats, on='cluster_id', how='left')

    return df

def evaluate_clusters(df: pd.DataFrame):
    """Évalue qualité des clusters (pour le mémoire)."""
    n_clusters = df[df['cluster_id'] != -1]['cluster_id'].nunique()
    n_noise = (df['cluster_id'] == -1).sum()
    noise_ratio = n_noise / len(df)

    print(f"Clusters trouvés : {n_clusters}")
    print(f"Points bruit : {n_noise} ({noise_ratio:.1%})")
    print(f"Taille moyenne cluster : {df[df['cluster_id'] != -1].groupby('cluster_id').size().mean():.1f}")

    return n_clusters, noise_ratio
```

---

## Métriques de Validation

| Métrique | Cible | Signification |
|----------|-------|---------------|
| Silhouette score | > 0.50 | Cohérence intra-cluster |
| Ratio bruit | < 20% | Pas trop de points isolés |
| Nb clusters / nb points | Raisonnable | Pas de sur-clustering |

---

*JeryMotroNet → [[04_JeryMotroNet]]*
*Feature Engineering → [[06_Feature_Engineering]]*
