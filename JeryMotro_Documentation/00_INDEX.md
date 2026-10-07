# Documentation JeryMotro — fonctionnement réel et architecture technique

> Référence : 7 octobre 2026. Les descriptions privilégient le code, les configurations et les workflows vérifiables. Pour le **déploiement présenté dans cette documentation**, la référence réseau demandée est la variante **DuckDNS + Nginx**.

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
- [16 Déploiement GCP / DuckDNS](16_DEPLOIEMENT_GCP_DEBIAN13.md)
- [17 Hugging Face](17_HUGGING_FACE_DATA_ET_SCRIPTS.md)
- [18 Nginx et routage](18_NGINX_ET_ACCES_RESEAU.md)
- [19 Sécurité](19_SECURITE_SECRETS_ET_CONFIGURATION.md)
- [20 Limites et état réel](20_LIMITES_ET_ETAT_REEL.md)
- [21 Stack technique](21_STACK_TECHNIQUE.md)
- [22 Protocoles et interfaces](22_PROTOCOLLES_ET_INTERFACES.md)
- [23 Stratégie de déploiement DuckDNS](23_STRATEGIE_DEPLOIEMENT_DUCKDNS.md)
- [24 SEO, prerender, sitemap et robots](24_SEO_PRERENDER_SITEMAP_ROBOTS.md)
- [25 Cahier des charges fonctionnel et technique](25_CAHIER_DES_CHARGES.md)
- [Glossaire des tags](Glossaire_Tags.md)

## Diagrammes
Les PlantUML se trouvent dans [plantuml/](plantuml/) :
architecture globale, pipeline opérationnel, ingestion FIRMS, scoring ML, clustering, enrichissement GEE, alertes, Chat RAG, frontend/backend, déploiement et Nginx.

## Hiérarchie des preuves
1. Code d'exécution.
2. Configuration versionnée réellement utilisée comme référence.
3. Scripts/workflows de déploiement.
4. UML et documentation technique.
5. Notes de conception historiques.

## Classes d'affirmation
- **Réel** : visible directement dans le code.
- **Intégration** : code présent et dépendant d'un service externe/secret.
- **Déploiement de référence** : topologie explicitement retenue pour cette documentation.
- **Séparé** : traitement existant hors pipeline principal.
- **Conception** : intention sans preuve suffisante d'exécution.
- **Historique/variante** : autre chaîne présente dans le dépôt, mais non retenue ici.

> **Anti-hallucination :** une présence dans un fichier de configuration ne prouve pas à elle seule l'activité de tout le service. Les responsabilités sont documentées avec leur niveau de preuve.

> **Sécurité :** ne jamais écrire les valeurs réelles des secrets.

---

## Navigation Obsidian

La série technique est navigable linéairement avec les liens `← Précédent | Index | Suivant →` placés en bas de chaque note. Le [[25_CAHIER_DES_CHARGES|cahier des charges]] clôt la série et renvoie vers le [[Glossaire_Tags|glossaire des tags]].

**Entrée recommandée :** [[01_VISION_GENERALE]] → [[02_FONCTIONNEMENT_REEL]] → [[03_ARCHITECTURE_TECHNIQUE]] → … → [[25_CAHIER_DES_CHARGES]].

- [26 Bibliographie et webographie APA](26_BIBLIOGRAPHIE_WEBOGRAPHIE_APA.md)
