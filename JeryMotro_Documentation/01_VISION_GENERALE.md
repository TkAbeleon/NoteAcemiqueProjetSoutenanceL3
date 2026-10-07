# Vision générale de JeryMotro

JeryMotro est une plateforme de suivi et d'analyse des feux de végétation à Madagascar. Le backend exploite notamment les détections satellitaires NASA FIRMS, les valide géographiquement, leur attribue une région, demande un score de risque à un service ML externe, regroupe les détections en événements et expose ces résultats à l'application Web.

## Chaîne fonctionnelle
**Observer → Valider → Analyser → Regrouper → Suivre → Alerter**

## Composants
- Frontend React/Vite
- Backend FastAPI
- SQLAlchemy + base SQL
- NASA FIRMS
- service ML externe
- scripts Google Earth Engine
- n8n
- WAHA
- SMS configuré
- Nginx

## Rôle de l'IA
Le ML sert au scoring du risque. Le Chat IA est un autre flux : le backend le relaie vers n8n.

## Limites
JeryMotro ne constitue pas à lui seul une preuve terrain d'un feu, de son extinction ou d'une prédiction parfaite. Les traitements fournissent de l'aide à l'analyse et la décision.

## Formulation de soutenance
> JeryMotro transforme des observations satellitaires en informations cartographiques et analytiques, avec des couches de Machine Learning, de regroupement spatial, de suivi temporel et de notification.