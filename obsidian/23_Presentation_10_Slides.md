# 📑 Rapport de Projet : JeryMotro (Format 10 Pages)
#JeryMotro #MemoireL3 #Rapport #Architecture
[[Glossaire_Tags]] | [[00_INDEX]]

> **Instructions** : Ce document est structuré pour générer un rapport de projet au format présentation (PPTX) ou PDF de 10 pages. Contrairement à une présentation orale, ces pages contiennent des descriptions techniques et formelles du travail accompli.

---

## Page 1 : Page de Garde et Résumé Exécutif
**Titre** : JeryMotro — Plateforme Intelligente de Surveillance et Prédiction des Feux de Brousse.
**Résumé Exécutif** : 
Le projet JeryMotro vise à fournir une solution technologique bout-en-bout pour le suivi des anomalies thermiques à Madagascar. En s'appuyant sur des données satellitaires de la NASA (MODIS/VIIRS) et une architecture moderne découplée, la plateforme permet l'agrégation, la prédiction de risque via apprentissage automatique (Machine Learning), et l'alerte proactive. Ce rapport documente l'architecture, les composants déployés et les perspectives de la plateforme.

---

## Page 2 : Contexte et Définition du Besoin
**Titre de la section** : Analyse du Besoin
**Contenu** :
- **L'Enjeu Environnemental** : Madagascar subit des dégradations forestières massives dues aux feux de brousse (pratique du Tavy). La surveillance manuelle est insuffisante sur un tel territoire.
- **Limites Actuelles** : Les flux de données de la NASA (FIRMS) sont publics mais bruts, livrés sans contexte local ni évaluation du risque d'incendie majeur.
- **La Réponse Technologique** : Construire un outil digital autonome (JeryMotro) qui collecte, nettoie, stocke et évalue ces données, tout en fournissant une interface de suivi "Cyber-Analytique" intuitive pour les acteurs de la conservation.

---

## Page 3 : L'Architecture Système Globale (V2)
**Titre de la section** : Topologie de l'Architecture Découplée
**Contenu** :
L'architecture de JeryMotro (V2) s'oriente vers des micro-services découplés pour maximiser la performance de l'Intelligence Artificielle :
1. **Pipeline de Données** : Orchestration via `n8n` pour la collecte ETL (Extract, Transform, Load).
2. **Stockage Central** : Base de données `PostgreSQL` hébergée sur Supabase, incluant l'extension spatiale `PostGIS`.
3. **Moteur Backend** : API asynchrone développée en Python avec `FastAPI` et `SQLAlchemy`.
4. **Interface Utilisateur** : Application Web réactive (`React` / Interface prototype `Symfony` existante).

---

## Page 4 : Le Pipeline de Collecte Automatisée (n8n)
**Titre de la section** : Automatisation et Ingestion des Données
**Contenu** :
L'ingestion des données satellitaires est totalement automatisée pour garantir la fraîcheur de l'information (temps quasi-réel) :
- **Source des données** : API FIRMS (NASA) couvrant les instruments MODIS, VIIRS_SNPP et VIIRS_NOAA21.
- **Orchestration** : Un workflow n8n s'exécute via un "Cronjob" toutes les 3 heures.
- **Traitement (Pre-processing)** : Les requêtes HTTP récupèrent les données au format CSV. Le script gère la déduplication et filtre le bruit (suppression des données à faible niveau de confiance) avant l'insertion en base de données.

---

## Page 5 : Le Backend et la Base de Données (FastAPI)
**Titre de la section** : Le Noyau Fonctionnel API
**Contenu** :
Le backend FastAPI agit comme le chef d'orchestre des données. Il sécurise l'accès et formate les flux pour le front-end.
- **Modèle de Données** : Les tables critiques comprennent `firms_fire_detections` (données brutes), `firms_hotspots` (clusters) et `alerts` (historique des notifications).
- **Routes Développées** :
  - `/api/detections` & `/api/clusters` : Accès en lecture seul aux données géospatiales.
  - `/api/alerts` : Gestion de l'historique de communication.
- **Sécurité et Performance** : Typage strict avec `Pydantic` et génération automatique de la documentation Swagger/OpenAPI.

---

## Page 6 : L'Intelligence Artificielle de Prédiction (MadFireNet)
**Titre de la section** : Modélisation du Risque Incendie
**Contenu** :
La valeur ajoutée de JeryMotro réside dans l'inférence du risque d'un feu détecté.
- **Modèle ML** : Utilisation de l'algorithme de classification `XGBoost`.
- **Ingénierie des Caractéristiques (Feature Engineering)** : L'algorithme prend en compte 18 variables indépendantes, incluant la puissance radiative du feu (FRP), les données météorologiques (ERA5), et les indices de végétation (NDVI Sentinel-2).
- **Résultat** : Chaque détection est enrichie d'un `risk_score` (probabilité de 0 à 1) permettant au système de catégoriser l'urgence en Modérée, Élevée ou Critique.

---

## Page 7 : L'Agent Intelligent Conversationnel (RAG)
**Titre de la section** : JeryMotro AI (Chatbot Contextuel)
**Contenu** :
Pour faciliter l'interprétation des données complexes, un assistant intelligent basé sur la génération augmentée par la recherche (RAG) a été implémenté.
- **Infrastructure IA** : Utilisation du LLM `Llama-3` via l'API ultra-rapide de `Groq`.
- **Mémoire Vectorielle** : `ChromaDB` sert de base de connaissances locale pour ancrer les réponses de l'IA sur les données strictes du projet.
- **Fonctionnalité** : L'Agent interroge la base pour fournir des statistiques en langage naturel, des résumés d'activités quotidiens, et des recommandations sur-mesure.

---

## Page 8 : L'Interface Utilisateur et l'Expérience (UI/UX)
**Titre de la section** : Visualisation Cyber-Analytique
**Contenu** :
L'interface de la plateforme est pensée pour un usage en salle de contrôle comme sur le terrain.
- **Ergonomie** : Un mode "Sombre" limitant la fatigue oculaire et permettant de faire ressortir visuellement les points de chaleur (rouge/orange) sur la cartographie.
- **Modules de la Plateforme** :
  - *Dashboard interactif* pour le suivi cartographique (HDBSCAN Clustering).
  - *Console d'Alertes* pour le suivi des urgences.
  - *Espace IA* pour converser avec les bases de données.

---

## Page 9 : Le Système de Routage des Alertes
**Titre de la section** : Notifications et Diffusion de l'Information
**Contenu** :
Afin de transformer la donnée en action, le système embarque une logique de communication automatique conditionnée par le score de risque (`risk_score`).
- **Logique de déclenchement** : Si une détection dépasse un score critique (ex: >0.8), une routine d'alerte est immédiatement exécutée par le backend ou n8n.
- **Multicanal** : L'information est disséminée selon sa gravité via :
  - **Email** : Pour l'administration forestière (rapports détaillés).
  - **WhatsApp / SMS (Twilio)** : Pour les équipes d'intervention locales nécessitant une réactivité immédiate.

---

## Page 10 : Bilan et Perspectives du Projet
**Titre de la section** : Conclusion et Évolutions
**Contenu** :
- **État d'avancement** : La plateforme a prouvé la viabilité de son architecture technique (Collecte n8n fonctionnelle, API déployée, prototype d'interface en ligne).
- **Prochaines étapes (Short-Term)** : Intégration complète du modèle XGBoost finalisé au sein du backend FastAPI et bascule sur un client lourd React interactif.
- **Vision à Long Terme** : 
  - Développer le réseau neuronal `ConvLSTM` pour prédire la propagation spatiale (grille) à J+1.
  - Déploiement pilote en collaboration avec les parcs nationaux malgaches (MNP) pour valider l'impact sur le terrain.
