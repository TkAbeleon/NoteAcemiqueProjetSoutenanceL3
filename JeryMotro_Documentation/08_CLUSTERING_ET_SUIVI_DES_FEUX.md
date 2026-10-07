# Clustering et suivi des événements feu

## Clustering
`cluster_service.py` utilise HDBSCAN lorsque disponible.

Paramètres observés :
- min_cluster_size = 3 ;
- min_samples = 1 ;
- cluster_selection_epsilon = 0.

La métrique est euclidienne sur latitude/longitude.

## Fallback
Si HDBSCAN n'est pas disponible, le backend utilise une grille de 0.05° environ. Les singletons sont du bruit dans ce fallback.

## Bruit
Le label -1 donne `is_noise = 1`. Les points bruit ne deviennent pas des FireEvent.

## FireEvent
Pour un groupe, le backend calcule notamment :
- centroïde ;
- taille ;
- FRP total et maximum ;
- risque maximum ;
- niveau ;
- région majoritaire ;
- first_seen / last_seen ;
- durée ;
- heures depuis la dernière observation ;
- statut et raison.

## Statut
- ACTIVE ≤ 9 h ;
- COOLING > 9 h et ≤ 72 h ;
- LIKELY_OUT > 72 h ;
- UNKNOWN si le pipeline n'est pas sain.

## Réactivation
`check_reactivation()` reconnaît le cas LIKELY_OUT + nouvelle détection.

Cela ne suffit pas à prouver un workflow métier plus complexe.

## Limite
Un cluster informatique est une agrégation ; ce n'est pas une preuve physique qu'il n'existe qu'un seul incendie.

---

**Navigation :** [[07_ML_SCORING_RISQUE|← Précédent]] | [[00_INDEX|Index]] | [[09_ENRICHISSEMENT_GEE_ENVIRONNEMENT|Suivant →]]
