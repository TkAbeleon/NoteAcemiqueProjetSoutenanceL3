# Architecture technique de JeryMotro

## 1. Architecture logique

JeryMotro est une architecture Web multi-services. Le navigateur n'accède pas directement à PostgreSQL, au service ML, à la base vectorielle ou aux services de notification : Nginx fournit le point d'entrée HTTPS et distribue vers les services exposés.

```
                         Internet
                            |
                         HTTPS/443
                            |
                        +---v---+
                        | Nginx |
                        +---+---+
                            |
          +-----------------+------------------+
          |                 |                  |
          v                 v                  v
   Frontend Web       FastAPI :8200      Services externes
   React/Vite             |             / locaux associés
                           |
          +----------------+-----------------------------+
          |                |          |       |           |
          v                v          v       v           v
      Base SQL         NASA FIRMS   ML API   n8n        WAHA
                                      |       |           |
                                      |       +--> DB feu |
                                      |       +--> Qdrant |
                                      |       +--> modèle IA
                                      |
                                   scoring
```

Le bloc « n8n → DB feu / Qdrant » correspond au fonctionnement du Chat confirmé pour le déploiement : n8n dispose du contexte de la base des feux pour les questions portant sur les données du système et utilise Qdrant lorsque la question nécessite la base de connaissances.

## 2. Frontend

Le dépôt `JeryMotro_WEB` est organisé comme un workspace pnpm.

Technologies réellement déclarées :
- React 19.1.0 ;
- React DOM 19.1.0 ;
- Vite 7.3.2 ;
- TypeScript 5.9.3 ;
- Wouter 3.3.5 ;
- TanStack React Query 5.90.21 ;
- Zod 3.25.76 ;
- Tailwind CSS 4.1.14 ;
- Framer Motion 12.23.24 ;
- Lucide React 0.545.0.

Le workspace utilise aussi des bibliothèques Recharts/Leaflet dans les paquets d'interface du projet.

## 3. Backend

Le backend est une API FastAPI exécutée par Uvicorn.

Dépendances techniques déclarées dans `Backend/api/requirements.txt` :
- FastAPI >= 0.104.0 ;
- Starlette >= 0.35.0 ;
- Uvicorn >= 0.24.0 ;
- SQLAlchemy >= 2.0.27 ;
- Alembic >= 1.13.1 ;
- asyncpg >= 0.29.0 ;
- aiosqlite >= 0.20.0 ;
- Pydantic >= 2.6.0 ;
- Pydantic Settings >= 2.2.0 ;
- httpx >= 0.27.0 ;
- pandas >= 2.2.0 ;
- numpy >= 1.26.0 ;
- scikit-learn >= 1.3.0 ;
- Shapely >= 2.0.0 ;
- Earth Engine API >= 1.4.0 ;
- google-auth >= 2.29.0 ;
- google-cloud-aiplatform >= 1.51.0 ;
- PyJWT 2.8.0 ;
- bcrypt 4.0.1.

## 4. Architecture du backend

Le point d'entrée `api/main.py` :
- initialise la base ;
- lance les migrations selon configuration ;
- exécute les checks de démarrage ;
- crée les tables ;
- lance la maintenance géographique ;
- démarre le collecteur FIRMS ;
- charge les routers métier.

Le backend est donc à la fois :
- API REST ;
- orchestrateur du pipeline FIRMS ;
- couche d'accès aux données ;
- passerelle vers plusieurs services.

## 5. Persistance SQL

SQLAlchemy 2.x est utilisé avec une session asynchrone.

Le driver PostgreSQL principal est `asyncpg`.

Le code normalise `postgresql://` / `postgres://` vers `postgresql+asyncpg://` et convertit `sslmode` en paramètre de connexion compatible asyncpg.

Le moteur utilise :
- `pool_pre_ping=True` ;
- `pool_recycle=300` ;
- sessions asynchrones.

La cible réelle de production est déterminée par `DATABASE_URL`.

## 6. Accès au Chat

Le chemin applicatif est :

```
React
  |
  | HTTP(S) JSON
  v
POST /chat
  |
  v
FastAPI
  |
  | HTTP(S) webhook JSON
  v
n8n
  |
  +--> base de données des feux
  |
  +--> Qdrant (base de connaissances)
  |
  +--> modèle IA
```

Le backend n'exécute pas directement la recherche vectorielle dans `rag_service.py`. Il transmet la requête et le contexte au workflow n8n.

## 7. Machine Learning

`jerymotronet_service.py` est un client HTTP asynchrone.

Le backend envoie des instances à `POST <ML_SERVICE_URL>/predict` et récupère `risk_score` et `fire_label`.

## 8. Géospatial

Le backend utilise Shapely + GeoJSON pour le point-in-polygon.

Le commentaire de `main.py` indique que Layerbase ne fournit pas PostGIS pour cette fonction.

## 9. Compression et middleware

FastAPI ajoute :
- CORSMiddleware ;
- GZipMiddleware avec compression à partir d'une taille minimale.

## 10. Architecture réseau

Le fichier `UML_JeryMotro/conf.ngnix` conserve l'architecture de routage de production :

| Domaine | Cible locale |
|---|---|
| jerymotro.duckdns.org | build frontend |
| api.jerymotro.duckdns.org | localhost:8200 |
| rag.jerymotro.duckdns.org | localhost:6333 |
| waha.jerymotro.duckdns.org | localhost:3001 |
| chat.jerymotro.duckdns.org | localhost:8065 |
| n8n.jerymotro.duckdns.org | localhost:5678 |
| api.smsgate.jerymotro.duckdns.org | localhost:3030 |
| smsgate.jerymotro.duckdns.org | localhost:3031 |

Nginx termine TLS et route les requêtes par nom de domaine.

## 11. Responsabilités

| Composant | Responsabilité |
|---|---|
| React/Vite | interface utilisateur |
| FastAPI/Uvicorn | API + orchestration backend |
| SQLAlchemy/DB | persistance |
| NASA FIRMS | source de détections |
| service ML | scoring |
| GEE scripts | enrichissement environnemental séparé |
| n8n | orchestration Chat/automatisations |
| DB des feux | données métier utilisées par les traitements |
| Qdrant | base vectorielle pour la connaissance |
| WAHA | API WhatsApp |
| SMSGate/HTTPSMS | SMS |
| Nginx | reverse proxy + TLS |

## 12. Point de méthode

Un composant logiciel peut exister dans les dépendances sans être utilisé dans tous les scénarios. Par exemple, `chromadb` apparaît dans les requirements historiques du backend, alors que le `rag_service.py` actuel n'instancie pas de client ChromaDB.

La documentation utilise donc les rôles réellement observés dans le code d'exécution plutôt que les seules dépendances installées.