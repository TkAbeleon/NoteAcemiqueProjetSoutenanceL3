# 📈 Rapport d'Avancement Global — JeryMotro Platform
#JeryMotro #MemoireL3 #Rapport #Avancement #Architecture #Symfony #FastAPI
[[Glossaire_Tags]] | [[00_INDEX]]

---

> **Date** : 2 Mai 2026
> **Objectif** : Synthétiser l'état de l'art du prototype actuel (Symfony) et détailler techniquement la fondation du nouveau backend (FastAPI) fraîchement développé.

---

## 1. 🖥️ Le Prototype Existant (Symfony V1)

Le projet possède déjà un prototype complet et fonctionnel déployé en ligne (HuggingFace). Il s'agit d'une application monolithique avec un thème "Cyber-Analytique" sombre très immersif. 

### Fonctionnalités Actuelles du Prototype Symfony :
1. **Dashboard Principal** : Affiche les statistiques globales de télédétection spatiale, chargement asynchrone des données de feu.
2. **Système d'Alertes (`/alerts`)** : 
   - Historique tabulaire des 50 dernières alertes.
   - Affichage du destinataire, du message, de l'ID de la détection concernée et d'un badge de statut (*Envoyé* / *Échoué*).
   - Bouton de déclenchement manuel d'alerte.
3. **Agent IA JeryMotro (`/agent`)** : 
   - Interface conversationnelle.
   - Boutons de prompts rapides (*Feux d'aujourd'hui*, *Hotspots critiques*, *Stats hebdos*, *Alertes*).
   - L'Agent retourne une réponse structurée en 3 parties (Résultat chiffré, Analyse textuelle, Recommandation stratégique).
4. **Gestion des Utilisateurs (`/users`)** : Interface d'administration et de visualisation des contacts cibles.
5. **Génération PDF (`/export/pdf`)** : Possibilité d'exporter les données sous forme de rapports.

---

## 2. ⚙️ Collecte Automatique des Données (n8n)

En amont de toute interface, la plateforme est alimentée par une machinerie DevOps robuste :
- **n8n Automation** : Des workflows quotidiens tournent pour télécharger les données satellitaires brutes de la NASA (FIRMS).
- **Base de Données Centrale** : Une base de données PostgreSQL gérée par **Supabase** sert de point de rassemblement. Elle contient 12 tables dont les plus critiques sont `firms_fire_detections` (points bruts) et `firms_hotspots` (points groupés par densité).

---

## 3. 🐍 Le Nouveau Moteur : Backend FastAPI (V2)

Pour dépasser les limites d'un monolithe Symfony et intégrer le véritable Machine Learning Python (XGBoost), un **Backend API découplé** vient d'être développé et testé avec succès sur la base Supabase.

### A. Structure Technique & Choix Technologiques
- **Framework** : `FastAPI` (pour sa rapidité asynchrone et sa documentation Swagger automatique).
- **ORM** : `SQLAlchemy` (pour la liaison entre les objets Python et la base PostgreSQL).
- **Validation** : `Pydantic` (pour la vérification stricte des données entrantes et sortantes).

### B. Les Endpoints Détaillés (Routes)
Le backend expose désormais les 5 domaines fondamentaux de la plateforme :

1. **`GET /api/detections`** 
   - *Rôle* : Interroge la table `firms_fire_detections`.
   - *Fonctionnement* : Renvoie la liste des points de feu bruts (MODIS/VIIRS) avec leur FRP (Fire Radiative Power) et le niveau de confiance.
2. **`GET /api/clusters`**
   - *Rôle* : Interroge la table `firms_hotspots`.
   - *Fonctionnement* : Regroupe visuellement les feux actifs (FRP élevé) pour limiter le bruit sur la carte.
3. **`GET /api/alerts`**
   - *Rôle* : Interroge la table `alerts`.
   - *Fonctionnement* : Retourne l'historique complet des alertes générées par le système.
4. **`POST /api/predictions` (MadFireNet)**
   - *Rôle* : Cerveau de prédiction XGBoost.
   - *Fonctionnement* : Reçoit 18 features (FRP, température, NDVI, etc.), passe ces données au `madfirenet_service` et retourne un `risk_score` de 0 à 1 (ex: `0.85 -> Risque ÉLEVÉ`).
5. **`POST /api/chat` (JeryMotro AI RAG)**
   - *Rôle* : Le nouveau cerveau du Chatbot.
   - *Fonctionnement* : Prend une question en langage naturel, passe par le `rag_service` pour interroger la base vectorielle (ChromaDB) et génère une réponse experte via le LLM Groq (Llama-3).

### C. Services & Logique Métier
- **`madfirenet_service.py`** : Conçu pour charger dynamiquement le modèle `.pkl` (fichier entraîné). Actuellement en mode simulation, il applique une logique de pondération stricte pour classer le feu (Modéré, Élevé, Critique).
- **`rag_service.py`** : Intègre le système RAG (Retrieval-Augmented Generation). Il est scripté avec le prompt système limitant strictement l'IA aux seules données de Madagascar.

---

## 4. 🎯 Conclusion & Prochaines Étapes

Le **Prototype Symfony (V1)** nous offre une interface de démonstration sublime et un flux logique clair. Le **Backend FastAPI (V2)**, quant à lui, apporte la puissance de calcul IA et la scalabilité nécessaires au Machine Learning.

**La suite du développement :**
1. Création de l'interface **React/Leaflet** (le Frontend V2) en s'inspirant du design Symfony.
2. Entraînement final de **MadFireNet (XGBoost)** et intégration du fichier `.pkl` réel dans FastAPI.
3. Mise en place de la base vectorielle locale **ChromaDB** pour le chat.
