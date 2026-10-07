# Documentation JeryMotro — fonctionnement réel

> Référence : 7 octobre 2026. Cette documentation privilégie le code actuel, puis la configuration et les workflows. Les anciennes notes servent uniquement de contexte.

## Navigation
- [01 Vision générale](01_VISION_GENERALE.md)
- [02 Fonctionnement réel](02_FONCTIONNEMENT_REEL.md)
- [03 Architecture technique](03_ARCHITECTURE_TECHNIQUE.md)
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
- [16 Déploiement GCP](16_DEPLOIEMENT_GCP_DEBIAN13.md)
- [17 Hugging Face](17_HUGGING_FACE_DATA_ET_SCRIPTS.md)
- [18 Nginx](18_NGINX_ET_ACCES_RESEAU.md)
- [19 Sécurité](19_SECURITE_SECRETS_ET_CONFIGURATION.md)
- [20 Limites et état réel](20_LIMITES_ET_ETAT_REEL.md)

## Classement des affirmations
- **Réel** : visible directement dans le code/configuration.
- **Intégration** : code présent, dépend d'un service ou secret externe.
- **Séparé** : script présent mais hors pipeline principal.
- **Conception** : prévu/documenté sans preuve suffisante d'exécution.
- **Historique** : ancienne configuration.

## Sources
Backend : TkAbeleon/JeryMotroBackend  
Frontend : TkAbeleon/JeryMotro_WEB  
Notes/UML : ce dépôt, notamment UML_JeryMotro/

> Ne jamais recopier de secret réel dans cette documentation.