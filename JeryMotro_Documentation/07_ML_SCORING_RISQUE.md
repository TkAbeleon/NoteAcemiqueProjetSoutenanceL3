# Machine Learning et scoring du risque

## Architecture
Le backend n'entraîne pas XGBoost dans le routeur principal étudié. Il appelle un microservice ML externe via `jerymotronet_service.py`.

Contrat principal :
`POST <ML_SERVICE_URL>/predict`.

Modèle configuré par défaut : `xgboost-v1`.

## Entrées
Le scoring peut utiliser notamment latitude, longitude, FRP, brightness, date, daynight, satellite, instrument, confiance et variables environnementales lorsqu'elles sont disponibles.

## Sorties
- `risk_score`
- `fire_label`

## Fallback
En cas de panne du service ou de score négatif, `internal.py` calcule une heuristique basée notamment sur FRP et confiance.

## Niveaux
`compute_risk_level()` :
- FRP > 50 : CRITICAL ;
- score invalide/négatif : UNKNOWN ;
- score ≥ 0.80 : CRITICAL ;
- score ≥ 0.60 : HIGH ;
- score ≥ 0.40 : MEDIUM ;
- sinon LOW.

## Métriques
Le dépôt backend inspecté ne contient pas le protocole complet d'entraînement/évaluation permettant de justifier une accuracy académique. Une valeur affichée dans le frontend ne doit donc pas être présentée comme mesure scientifique.

## Deep Learning
Le contrat `/predict-grid` existe côté client ML et les notes de conception parlent de ConvLSTM/J+1. Cela ne prouve pas une génération automatique J+1 complète en production.