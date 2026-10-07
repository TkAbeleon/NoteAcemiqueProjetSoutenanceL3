# Documentation JeryMotro — fonctionnement réel et architecture technique

> Référence : 7 octobre 2026. Cette documentation privilégie le code actuel, puis la configuration et les workflows. Les anciennes notes servent uniquement de contexte.

## Navigation fonctionnelle
- [01 Vision générale](01_VISION_GENERALE.md)
- [02 Fonctionnement réel](02_FONCTIONNEMENT_REEL.md)
- [04 Pipeline de données](04_PIPELINE_DONNEES.md)
- [05 FIRMS et BDD](05_DONNEES_FIRMS_ET_BDD.md)
- [06 Géolocalisation](06_GEOLOCALISATION_ET_VALIDATION.md)
- [07 ML et scoring](07_ML_SCORING_RISQUE.md)
- [08 Clustering](08_CLUSTERING_ET_SUIVI_DES_FEUX.md)
- [09 Enrichissement GEE](09_ENRICHISSEMENT_GEE_ENVIRONNEMENT.md)
- [10 Statistiques](10_STATISTIQUES_ET_ANALYSE.md)
- [11 Alertes](11_ALERTES_ET_NOTIFICATIONS.md)
- [12 Chat IA/RAG](12_CHAT_IA_RAG.md)
- [13 Frontend](13_FRONTEND_ET_INTERFACE.md)
- [14 Authentification](14_AUTHENTIFICATION_ROLES_ACCES.md)
- [15 Prédictions J+1](15_PREDICTIONS_J_PLUS_1.md)

## Navigation technique
- [03 Architecture technique](03_ARCHITECTURE_TECHNIQUE.md)
- [16 Déploiement GCP Debian 13](16_DEPLOIEMENT_GCP_DEBIAN13.md)
- [17 Hugging Face](17_HUGGING_FACE_DATA_ET_SCRIPTS.md)
- [18 Nginx et routage](18_NGINX_ET_ACCES_RESEAU.md)
- [19 Sécurité et configuration](19_SECURITE_SECRETS_ET_CONFIGURATION.md)
- [21 Stack technologique](21_STACK_TECHNIQUE.md)
- [22 Protocoles et interfaces](22_PROTOCOLLES_ET_INTERFACES.md)
- [20 Limites et état réel](20_LIMITES_ET_ETAT_REEL.md)

## Diagrammes
Les schémas techniques sont dans [plantuml/](plantuml/), notamment :
- architecture globale ;
- pipeline opérationnel ;
- ingestion FIRMS ;
- scoring ML ;
- clustering ;
- enrichissement GEE ;
- alertes ;
- Chat IA/RAG ;
- frontend/backend ;
- déploiement ;
- routage Nginx.

## Hiérarchie des preuves
1. Code actuel.
2. Configuration actuelle/versionnée.
3. Workflows de déploiement.
4. UML et documentation de travail.
5. Notes historiques.

## Classes d'affirmation
- **Réel** : comportement visible directement dans le code/configuration.
- **Intégration** : code présent, dépend d'un service externe ou d'un secret.
- **Déploiement confirmé** : architecture fournie/confirmée pour la production.
- **Séparé** : script existant mais hors pipeline principal.
- **Conception** : objectif ou architecture non démontrée comme exécutée.
- **Historique** : ancienne configuration.

> **Règle anti-hallucination :** un composant mentionné dans une architecture n'est pas automatiquement une preuve d'exécution de chaque scénario. Les sections signalent donc explicitement les limites de preuve.

> **Règle de sécurité :** ne jamais écrire une valeur réelle de secret ; uniquement le nom de la variable ou un placeholder.