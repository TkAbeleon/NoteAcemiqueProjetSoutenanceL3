# Stack technologique JeryMotro

## 1. Vue d'ensemble

| Couche | Technologie / composant | Rôle |
|---|---|---|
| Frontend | React 19.1.0 | UI |
| Frontend | Vite 7.3.2 | build/dev server |
| Frontend | TypeScript 5.9.3 | typage |
| Frontend | Wouter 3.3.5 | routage |
| Frontend | TanStack React Query 5.90.21 | cache/requêtes serveur |
| Frontend | Tailwind CSS 4.1.14 | styles |
| Frontend | React Hook Form | formulaires |
| Frontend | Zod 3.25.76 | validation côté frontend |
| Cartographie | Leaflet 1.9.4 | moteur de carte |
| Cartographie | react-leaflet 5.0.0 | intégration React |
| Graphiques | Recharts 2.15.2 | visualisation |
| Documents | react-markdown 10.1.0 | rendu Markdown |
| PDF | @react-pdf/renderer 4.9.0 | génération PDF côté frontend |
| Backend | FastAPI | API HTTP |
| Backend | Uvicorn | serveur ASGI |
| Backend | Starlette | couche Web |
| Backend | Pydantic 2.x | schémas/configuration |
| Backend | SQLAlchemy 2.x | ORM |
| Migrations | Alembic | évolution du schéma |
| PostgreSQL | asyncpg | driver asynchrone |
| HTTP client | httpx | appels externes |
| Analyse | pandas | DataFrame/statistiques |
| Calcul numérique | NumPy | calculs numériques |
| ML local/fallback | scikit-learn | clustering disponible |
| Géospatial | Shapely | géométrie / point-in-polygon |
| GEE | Earth Engine API | enrichissement environnemental |
| Auth | PyJWT + bcrypt/passlib | JWT et mots de passe |
| Automatisation | n8n | workflows et Chat |
| Vector DB | Qdrant | base de connaissances vectorielle |
| WhatsApp | WAHA | envoi de messages |
| SMS | SMSGate / HTTPSMS | envoi SMS |
| Proxy/TLS | Nginx + Certbot | entrée HTTPS |
| Données | Hugging Face Datasets | stockage/partage de datasets |
| Déploiement HF | Docker Space | hébergement de certaines briques |

Les versions frontend viennent de `artifacts/jerymotro/package.json` et du catalog pnpm du workspace. Les dépendances backend viennent de `Backend/api/requirements.txt`.

## 2. Frontend

### React

React porte la couche présentation et l'état d'interface.

`App.tsx` configure :
- `QueryClientProvider` ;
- `ThemeProvider` ;
- `I18nProvider` ;
- `AuthProvider` ;
- routage Wouter ;
- chargement lazy des pages métier.

### Vite

Vite construit le bundle frontend.

Le script de build effectue également un build SSR puis un prerender des routes.

### React Query

Le frontend centralise les appels serveur dans un cache React Query.

La configuration observée utilise :
- `staleTime = 30 s` ;
- refresh en arrière-plan toutes les 5 min ;
- une tentative de retry supplémentaire pour les erreurs non-401.

### Cartographie

La page de carte active repose sur Leaflet et react-leaflet.

### Validation/UI

Le frontend utilise Zod, React Hook Form, Radix UI et Tailwind pour les formulaires et composants d'interface.

## 3. Backend

### FastAPI + Uvicorn

FastAPI expose l'API métier et Uvicorn fournit le serveur ASGI.

`run_server.py` appelle :

`uvicorn.run("api.main:app", host=settings.host, port=settings.port, ...)`

Le port par défaut du backend est 8200.

### SQLAlchemy

SQLAlchemy fournit l'ORM et les sessions asynchrones.

Le backend initialise un `AsyncEngine` et une `async_sessionmaker`.

### PostgreSQL / asyncpg

Pour PostgreSQL, le driver utilisé par l'application est asyncpg.

Le backend normalise l'URL PostgreSQL et convertit `sslmode` en `connect_args["ssl"]` pour la compatibilité asyncpg.

### Alembic

Alembic est présent pour les migrations.

Le démarrage peut appliquer automatiquement les migrations selon `AUTO_MIGRATE_ON_STARTUP` et `AUTO_MIGRATE_STRICT`.

## 4. Traitement scientifique

### pandas

Pandas est utilisé pour :
- ingestion CSV ;
- conversion/normalisation ;
- statistiques avancées ;
- gestion des valeurs manquantes.

### NumPy

NumPy intervient notamment dans le clustering et les calculs numériques.

### scikit-learn / HDBSCAN

Le clustering essaye `sklearn.cluster.HDBSCAN` puis le paquet `hdbscan`.

Un fallback par grille est prévu si les deux ne sont pas disponibles.

### Shapely

Shapely fournit les opérations géométriques côté Python avec les GeoJSON administratifs.

## 5. Intelligence artificielle

### ML

Le backend est un client du microservice ML et non le lieu d'entraînement du modèle.

### Chat / RAG

Le backend FastAPI relaie les requêtes à n8n.

n8n orchestre le Chat et possède les accès nécessaires :
- base relationnelle des données de feux ;
- Qdrant lorsque la question nécessite la base de connaissances ;
- modèle IA.

## 6. GEE

Les scripts d'enrichissement utilisent Earth Engine API, pandas, KaggleHub et tqdm.

Ils sont séparés du pipeline FastAPI principal.

## 7. Infrastructure

### Nginx

Nginx :
- reçoit le HTTPS ;
- termine TLS ;
- route les sous-domaines ;
- transmet les headers proxy ;
- gère certains WebSockets ;
- applique limites de taille et timeouts.

### Certbot

Certbot fournit/gère les certificats TLS référencés par Nginx.

### GCP Debian 13

L'environnement de production est une VM Google Cloud sous Debian 13, avec les services exposés via Nginx.

## 8. Hugging Face

Deux usages distincts :

### Dataset Hub
Conservation/partage de datasets.

### Docker Space
Déploiement d'un service conteneurisé. Le workflow GitHub vérifie `sdk: docker` et `app_port: 7860`.

## 9. Paquets présents mais rôle à distinguer

Le backend `requirements.txt` mentionne également `chromadb` et `google-cloud-aiplatform`.

Dans le `rag_service.py` actuel, aucun client ChromaDB ou Vertex AI n'est instancié directement.

La technologie installée et la technologie effectivement appelée dans un chemin d'exécution ne doivent donc pas être confondues.
