# Prédictions J+1

## Ce qui est présent
Le backend possède une entité `Prediction` et des routes de lecture notamment :
- `/predictions/latest`
- `/predictions/risk-map`

Le frontend possède une page Predictions.

## Ce que cela prouve
La plateforme possède une persistance et une exposition de résultats de prédiction.

## Ce que cela ne prouve pas
Le code étudié ne démontre pas, à lui seul, qu'un moteur complet génère automatiquement une nouvelle prédiction J+1 à chaque cycle.

Il ne faut donc pas présenter une génération nocturne systématique comme un fait sans preuve supplémentaire.

## Contrat de grille
`jerymotronet_service.py` contient `predict_convlstm_grid()`, qui appelle `POST <ML_SERVICE_URL>/predict-grid`.

Cela établit un contrat technique côté client, pas la preuve d'un modèle ConvLSTM complet actuellement planifié et alimenté.

## Conception
Les notes historiques décrivent une ambition ConvLSTM/J+1. Elles doivent rester séparées de l'état opérationnel.

## Pour prouver une chaîne J+1 complète
Il faudrait montrer modèle, préparation des séquences, endpoint de production, planification, stockage des sorties et évaluation reproductible.

---

**Navigation :** [[14_AUTHENTIFICATION_ROLES_ACCES|← Précédent]] | [[00_INDEX|Index]] | [[16_DEPLOIEMENT_GCP_DEBIAN13|Suivant →]]
