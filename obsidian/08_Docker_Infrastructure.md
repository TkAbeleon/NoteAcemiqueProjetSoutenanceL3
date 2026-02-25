# 🐳 Docker Infrastructure — JeryMotro Platform
#JeryMotro #MemoireL3 #Docker #DevOps
[[Glossaire_Tags]] | [[00_INDEX]] | [[02_Architecture_Globale]]

---

## 1. ARCHITECTURE DOCKER

```
madfire-network (réseau interne Docker)
│
├── madfire-db          PostgreSQL 15        port 5432
├── madfire-chromadb    ChromaDB             port 8001
├── madfire-api         FastAPI (Python)     port 8000
├── madfire-n8n         n8n                  port 5678
└── madfire-frontend    React / Flutter Web  port 3000
```

**Principe :** Les services communiquent entre eux par nom de service (DNS Docker interne).
Ex : depuis `madfire-api`, la BDD est accessible via `postgresql://madfire-db:5432/madfire`.

---

## 2. docker-compose.yml COMPLET

```yaml
version: "3.9"

services:

  # ─── BASE DE DONNÉES ───────────────────────────────────────
  madfire-db:
    image: postgres:15-alpine
    container_name: madfire-db
    restart: unless-stopped
    environment:
      POSTGRES_DB: ${POSTGRES_DB:-madfire}
      POSTGRES_USER: ${POSTGRES_USER:-madfire}
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD:-madfire_secret}
    volumes:
      - madfire_pgdata:/var/lib/postgresql/data
    networks:
      - madfire-network
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U madfire"]
      interval: 10s
      timeout: 5s
      retries: 5

  # ─── CHROMADB (RAG) ────────────────────────────────────────
  madfire-chromadb:
    image: chromadb/chroma:latest
    container_name: madfire-chromadb
    restart: unless-stopped
    volumes:
      - madfire_chromadb:/chroma/chroma
    ports:
      - "8001:8000"
    networks:
      - madfire-network

  # ─── FASTAPI BACKEND ───────────────────────────────────────
  madfire-api:
    build:
      context: ./api
      dockerfile: Dockerfile
    container_name: madfire-api
    restart: unless-stopped
    ports:
      - "8000:8000"
    environment:
      DATABASE_URL: postgresql://${POSTGRES_USER:-madfire}:${POSTGRES_PASSWORD:-madfire_secret}@madfire-db:5432/${POSTGRES_DB:-madfire}
      CHROMADB_HOST: madfire-chromadb
      CHROMADB_PORT: 8000
      GROQ_API_KEY: ${GROQ_API_KEY}
      FIRMS_MAP_KEY: ${FIRMS_MAP_KEY}
      TWILIO_ACCOUNT_SID: ${TWILIO_ACCOUNT_SID}
      TWILIO_AUTH_TOKEN: ${TWILIO_AUTH_TOKEN}
      ALERT_EMAIL: ${ALERT_EMAIL}
      SMTP_PASSWORD: ${SMTP_PASSWORD}
    volumes:
      - ./data:/app/data
      - ./ml/models_saved:/app/models_saved
    depends_on:
      madfire-db:
        condition: service_healthy
      madfire-chromadb:
        condition: service_started
    networks:
      - madfire-network

  # ─── FRONTEND (REACT) ──────────────────────────────────────
  madfire-frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile
    container_name: madfire-frontend
    restart: unless-stopped
    ports:
      - "3000:3000"
    environment:
      REACT_APP_API_URL: http://localhost:8000
    depends_on:
      - madfire-api
    networks:
      - madfire-network

  # ─── n8n AUTOMATISATION ────────────────────────────────────
  madfire-n8n:
    image: n8nio/n8n:latest
    container_name: madfire-n8n
    restart: unless-stopped
    ports:
      - "5678:5678"
    environment:
      DB_TYPE: postgresdb
      DB_POSTGRESDB_HOST: madfire-db
      DB_POSTGRESDB_PORT: 5432
      DB_POSTGRESDB_DATABASE: n8n
      DB_POSTGRESDB_USER: ${POSTGRES_USER:-madfire}
      DB_POSTGRESDB_PASSWORD: ${POSTGRES_PASSWORD:-madfire_secret}
      N8N_BASIC_AUTH_ACTIVE: "true"
      N8N_BASIC_AUTH_USER: admin
      N8N_BASIC_AUTH_PASSWORD: ${N8N_PASSWORD:-madfire_n8n}
      WEBHOOK_URL: http://localhost:5678
    volumes:
      - madfire_n8n:/home/node/.n8n
      - ./n8n/workflows:/workflows
    depends_on:
      madfire-db:
        condition: service_healthy
    networks:
      - madfire-network

volumes:
  madfire_pgdata:
  madfire_chromadb:
  madfire_n8n:

networks:
  madfire-network:
    driver: bridge
```

---

## 3. Dockerfile — FastAPI Backend

```dockerfile
# api/Dockerfile
FROM python:3.11-slim

WORKDIR /app

# Dépendances système pour geopandas + hdbscan
RUN apt-get update && apt-get install -y \
    gdal-bin \
    libgdal-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Dépendances Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Code source
COPY . .

# Migrations Alembic + démarrage
CMD ["sh", "-c", "alembic upgrade head && uvicorn main:app --host 0.0.0.0 --port 8000 --reload"]
```

---

## 4. Dockerfile — Frontend React

```dockerfile
# frontend/Dockerfile
FROM node:20-alpine AS builder

WORKDIR /app
COPY package*.json ./
RUN npm ci

COPY . .
RUN npm run build

# Production : nginx
FROM nginx:alpine
COPY --from=builder /app/build /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 3000
CMD ["nginx", "-g", "daemon off;"]
```

---

## 5. api/requirements.txt

```
fastapi==0.110.0
uvicorn[standard]==0.27.0
sqlalchemy==2.0.27
alembic==1.13.1
psycopg2-binary==2.9.9
pydantic==2.6.0
pydantic-settings==2.2.0
httpx==0.27.0
pandas==2.2.0
geopandas==0.14.3
shapely==2.0.3
hdbscan==0.8.33
xgboost==2.0.3
scikit-learn==1.4.0
torch==2.2.0
chromadb==0.4.22
sentence-transformers==2.5.1
groq==0.4.2
twilio==8.13.0
python-dotenv==1.0.1
pytest==8.0.0
httpx==0.27.0
```

---

## 6. .env.example

```bash
# NASA FIRMS
FIRMS_MAP_KEY=VOTRE_MAP_KEY_ICI

# NASA Earthdata
NASA_EARTHDATA_TOKEN=eyJ0eXAiOiJKV1Qi...

# Groq API
GROQ_API_KEY=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

# PostgreSQL
POSTGRES_DB=madfire
POSTGRES_USER=madfire
POSTGRES_PASSWORD=CHANGER_CE_MOT_DE_PASSE

# Twilio (Sandbox gratuit)
TWILIO_ACCOUNT_SID=ACXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
TWILIO_AUTH_TOKEN=XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
TWILIO_WHATSAPP_FROM=whatsapp:+14155238886

# Email Alertes
ALERT_EMAIL=alertes@votremail.com
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_PASSWORD=VOTRE_APP_PASSWORD_GMAIL

# n8n
N8N_PASSWORD=CHANGER_CE_MOT_DE_PASSE
```

---

## 7. Commandes Utiles

```bash
# Démarrer toute la stack
docker-compose up -d

# Voir les logs FastAPI en temps réel
docker-compose logs -f madfire-api

# Accéder à la BDD PostgreSQL
docker exec -it madfire-db psql -U madfire -d madfire

# Appliquer migrations Alembic
docker exec madfire-api alembic upgrade head

# Redémarrer un service après modification du code
docker-compose restart madfire-api

# Arrêter proprement
docker-compose down

# Tout supprimer y compris volumes (ATTENTION : efface les données)
docker-compose down -v
```

---

## 8. Ordre de Démarrage

```
1. madfire-db (PostgreSQL)         ← healthcheck requis
2. madfire-chromadb (ChromaDB)     ← démarrage immédiat
3. madfire-api (FastAPI)           ← attend db + chromadb
4. madfire-n8n (n8n)               ← attend db
5. madfire-frontend (React)        ← attend api
```

---

## 9. Accès aux Interfaces

| Service | URL | Description |
|---------|-----|-------------|
| FastAPI Swagger | http://localhost:8000/docs | Documentation API interactive |
| FastAPI ReDoc | http://localhost:8000/redoc | Documentation alternative |
| Frontend | http://localhost:3000 | Interface utilisateur |
| n8n | http://localhost:5678 | Gestion des workflows |

---

*Architecture → [[02_Architecture_Globale]]*
*FastAPI → [[09_FastAPI_Backend]]*
*Frontend → [[10_Frontend_Decision]]*
