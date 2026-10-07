# Géolocalisation et validation

## Premier filtre
La configuration backend fournit par défaut une bbox de Madagascar :
`43.2,-25.6,50.5,-11.9`.

## Validation
Avant insertion, `validate_and_label_fire_point()` vérifie le point et tente de lui attribuer une région.

## Données géographiques
Le backend utilise des fichiers GeoJSON administratifs locaux et Shapely.

## Fallback
BigDataCloud est prévu comme solution de reverse geocoding de repli selon la configuration.

## Nettoyage
Au démarrage, `main.py` peut lancer `cleanup_existing_fire_points()` en tâche de fond.

## Services
Les routes de région permettent de contrôler et de traiter les détections sans région.

## Interprétation
Les coordonnées sont celles des observations satellitaires et le rattachement régional est informatique. Cela ne remplace pas une vérification terrain.

---

**Navigation :** [[05_DONNEES_FIRMS_ET_BDD|← Précédent]] | [[00_INDEX|Index]] | [[07_ML_SCORING_RISQUE|Suivant →]]
