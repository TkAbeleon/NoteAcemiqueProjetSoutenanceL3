# Limites, écarts et état réel

## Principe
Cette page sépare explicitement les fonctions actuelles, les intégrations dépendantes, les scripts séparés et les perspectives.

## Collection FIRMS
**Réel :** collecte intégrée à la boucle automatique lorsqu'elle est activée.  
**Dépendances :** clé FIRMS, réseau, base, validation géographique et disponibilité du service.

## Enrichissement GEE
**Réel :** scripts GEE, extraction environnementale, fichiers enrichis.  
**À ne pas affirmer :** enrichissement synchrone de chaque nouvelle détection par le pipeline FastAPI.

## Machine Learning
**Réel :** appel HTTP vers le service ML, modèle configurable `xgboost-v1`, fallback heuristique.  
**À ne pas affirmer :** entraînement XGBoost dans FastAPI ou accuracy scientifique sans protocole d'évaluation.

## Clustering
**Réel :** HDBSCAN ou fallback grille, création/mise à jour de FireEvent, statut.  
**À valider :** qualité statistique du regroupement par rapport à une vérité terrain.

## Statut
**Réel :** ACTIVE ≤ 9 h, COOLING jusqu'à 72 h, LIKELY_OUT au-delà, UNKNOWN si pipeline non sain.  
**À ne pas affirmer :** qu'un feu est définitivement éteint après absence de détection.

## Alertes
**Réel :** abonnements, OTP, seuils, email n8n, WhatsApp WAHA, SMS configurable, déclenchement automatique et route admin.  
**Dépendances :** credentials, services externes et configuration utilisateur.

## Chat RAG
**Réel :** `POST /chat`, proxy n8n, contexte de zone, réponse normalisée, fallback.  
**À ne pas affirmer :** Qdrant/Vertex/Chroma exécutés directement par FastAPI.

## Déforestation
**Réel :** `is_recent_loss` comme contexte environnemental.  
**À ne pas affirmer :** détection autonome complète de la déforestation dans le pipeline principal.

## Prédiction J+1
**Réel :** persistance/routes de prédiction et contrat `/predict-grid`.  
**Non démontré :** génération planifiée complète J+1.

## Déploiement
**Réel/configuration fournie :** GCP Debian 13 déclaré, Nginx, sous-domaines et ports locaux.  
**Historique :** ancienne documentation Ubuntu 22.04, ancienne IP 35.192.27.164, PostgreSQL local.

## Validation scientifique
Les prochaines validations utiles portent sur couverture, faux positifs, faux négatifs, délai, qualité du clustering, performance ML, fiabilité des enrichissements et utilité des alertes.

## Formulation
> JeryMotro démontre plusieurs briques techniques de bout en bout, mais la validation scientifique, terrain et institutionnelle reste nécessaire avant de conclure à une performance opérationnelle généralisée.