# ⚡ FastAPI Backend — JeryMotro Platform
#JeryMotro #MemoireL3 #FastAPI #Python #API
[[Glossaire_Tags]] | [[00_INDEX]] | [[02_Architecture_Globale]]

---

## 1. RÔLE DE FASTAPI DANS L'ARCHITECTURE

FastAPI est le **pont central** entre :
- Les modèles ML/DL (JeryMotroNet) et la base de données
- Le frontend (React/Flutter) qui consomme les données
- L'IA générative (RAG + Groq) qui répond aux questions
- Le système d'alertes (Twilio + Email)

**Pourquoi FastAPI et pas Flask ou Django ?**

| Critère | FastAPI | Flask | Django |
|---------|---------|-------|--------|
| Performance async | ✅ Natif async/await | 🟡 Avec extensions | 🟡 Avec channels |
| Swagger auto | ✅ Généré auto | ❌ Manuel | 🟡 drf-spectacular |
| Validation Pydantic | ✅ Natif | ❌ Manuel | ❌ Manuel |
| Type hints | ✅ Obligatoires → doc auto | ❌ Optionnels | ❌ Optionnels |
| Apprentissage L3 | ✅ Simple + moderne | ✅ Simple | 🟡 Lourd |

---

## 2. STRUCTURE DE L'APPLICATION

```
api/
├── main.py                  # Point d'entrée FastAPI
├── database.py              # SQLAlchemy async engine
├── config.py                # Settings via Pydantic BaseSettings
│
├── routers/                 # Endpoints par domaine
│   ├── __init__.py
│   ├── detections.py        # GET /detections
│   ├── predictions.py       # GET /predictions, GET /risk-map
│   ├── clusters.py          # GET /clusters
│   ├── alerts.py            # GET /alerts
│   └── chat.py              # POST /chat
│
├── models/                  # SQLAlchemy ORM (tables BDD)
│   ├── __init__.py
│   ├── detection.py
│   ├── prediction.py
│   ├── cluster.py
│   └── alert.py
│
├── schemas/                 # Pydantic (validation I/O API)
│   ├── __init__.py
│   ├── detection.py
│   ├── prediction.py
│   └── chat.py
│
├── services/                # Logique métier
│   ├── madfirenet_service.py  # Inférence ML/DL
│   ├── rag_service.py         # ChromaDB + Groq
│   └── alert_service.py       # Email + Twilio
│
├── alembic/                 # Migrations BDD
│   └── versions/
│
├── tests/                   # Tests unitaires
│   ├── test_detections.py
│   ├── test_predictions.py
│   └── test_chat.py
│
├── requirements.txt
├── Dockerfile
└── .env (jamais committé)
```

---

## 3. main.py — Point d'Entrée

```python
# api/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from database import engine, Base
from routers import detections, predictions, clusters, alerts, chat

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup : créer tables si besoin
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    # Shutdown : fermer connexions

app = FastAPI(
    title="JeryMotro Platform API",
    description="API de détection intelligente des feux de brousse à Madagascar",
    version="2.2.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# CORS pour le frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://madfire.vercel.app"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inclusion des routers
app.include_router(detections.router, prefix="/detections", tags=["Détections"])
app.include_router(predictions.router, prefix="/predictions", tags=["Prédictions"])
app.include_router(clusters.router, prefix="/clusters", tags=["Clusters"])
app.include_router(alerts.router, prefix="/alerts", tags=["Alertes"])
app.include_router(chat.router, prefix="/chat", tags=["JeryMotro AI"])

@app.get("/", tags=["Santé"])
async def root():
    return {"status": "ok", "service": "JeryMotro Platform API v2.2"}

@app.get("/health", tags=["Santé"])
async def health():
    return {"status": "healthy", "version": "2.2.0"}
```

---

## 4. ENDPOINTS COMPLETS

### GET /detections

```python
# routers/detections.py
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
from datetime import date

router = APIRouter()

@router.get("/", summary="Récupère les détections FIRMS filtrées")
async def get_detections(
    date_from: Optional[date] = Query(None, description="Date début"),
    date_to: Optional[date] = Query(None, description="Date fin"),
    min_frp: float = Query(0.0, description="FRP minimum (MW)"),
    min_risk: float = Query(0.0, description="Score risque minimum (0–1)"),
    source: Optional[str] = Query(None, description="MODIS / VIIRS_SNPP / VIIRS_NOAA21"),
    limit: int = Query(1000, le=10000),
    db: AsyncSession = Depends(get_db)
):
    """
    Retourne les points de détection FIRMS avec leurs scores JeryMotroNet.
    """
    # ... requête SQLAlchemy
    return {"detections": results, "count": len(results)}
```

**Réponse JSON exemple :**
```json
{
  "detections": [
    {
      "id": 1,
      "latitude": -18.234,
      "longitude": 44.567,
      "brightness": 342.1,
      "frp": 87.3,
      "confidence": "high",
      "acq_date": "2026-02-23",
      "acq_time": "0845",
      "satellite": "NOAA-21",
      "daynight": "D",
      "risk_score": 0.84,
      "cluster_id": 5,
      "source": "VIIRS_NOAA21"
    }
  ],
  "count": 47
}
```

---

### GET /predictions

```python
@router.get("/", summary="Prédictions JeryMotroNet J+1")
async def get_predictions(
    date: Optional[date] = Query(None),
    region: Optional[str] = Query(None),  # ex: "Menabe", "Boeny"
    db: AsyncSession = Depends(get_db)
):
    """Retourne les prédictions de risque pour J+1."""
    ...
```

---

### GET /risk-map

```python
@router.get("/risk-map", summary="Carte risque ConvLSTM (grille 375m)")
async def get_risk_map(
    date: date = Query(...),
    format: str = Query("geojson", enum=["geojson", "json"])
):
    """
    Retourne la grille de risque J+1 prédite par ConvLSTM.
    Format GeoJSON pour Leaflet.
    """
    ...
```

---

### POST /chat

```python
# routers/chat.py
from schemas.chat import ChatRequest, ChatResponse
from services.rag_service import rag_query

@router.post("/", response_model=ChatResponse, summary="JeryMotro AI (RAG + Groq)")
async def chat_with_madfireai(request: ChatRequest):
    """
    Chat avec JeryMotro AI.
    Répond UNIQUEMENT sur les données du projet (RAG ChromaDB).
    """
    response = await rag_query(request.message)
    return ChatResponse(
        response=response.text,
        sources=response.sources,
        data_context=response.context
    )
```

**Schéma Pydantic :**
```python
# schemas/chat.py
from pydantic import BaseModel, Field

class ChatRequest(BaseModel):
    message: str = Field(..., min_length=3, max_length=500,
                         example="Quelle région est la plus touchée cette semaine ?")

class ChatResponse(BaseModel):
    response: str
    sources: list[str]      # Documents ChromaDB utilisés
    data_context: dict       # Données ML utilisées pour répondre
```

---

## 5. SERVICE RAG (Groq + ChromaDB)

```python
# services/rag_service.py
import chromadb
from groq import Groq
import os

chroma_client = chromadb.HttpClient(
    host=os.getenv("CHROMADB_HOST", "madfire-chromadb"),
    port=int(os.getenv("CHROMADB_PORT", 8000))
)
collection = chroma_client.get_or_create_collection("madfire_results")

groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))

SYSTEM_PROMPT = """
Tu es JeryMotro AI, un assistant spécialisé dans la détection des feux de brousse à Madagascar.
Tu réponds UNIQUEMENT en te basant sur les données du projet JeryMotro (résultats ML/DL, clusters, métriques).
Si la question dépasse les données du projet, réponds : "Je suis limité aux données JeryMotro."
Réponds toujours en français. Sois précis et cite les données.
"""

async def rag_query(question: str):
    # 1. Chercher contexte pertinent dans ChromaDB
    results = collection.query(
        query_texts=[question],
        n_results=5
    )
    context = "\n".join(results['documents'][0])

    # 2. Appel Groq avec contexte
    response = groq_client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"Contexte :\n{context}\n\nQuestion : {question}"}
        ],
        max_tokens=500,
        temperature=0.1   # Basse pour réponses précises
    )

    return response.choices[0].message.content
```

---

## 6. TESTS FASTAPI

```python
# tests/test_detections.py
import pytest
from httpx import AsyncClient
from main import app

@pytest.mark.asyncio
async def test_get_detections_empty():
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/detections/")
    assert response.status_code == 200
    assert "detections" in response.json()

@pytest.mark.asyncio
async def test_get_detections_filter_frp():
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/detections/?min_frp=50.0")
    data = response.json()
    assert all(d["frp"] >= 50.0 for d in data["detections"])

@pytest.mark.asyncio
async def test_health():
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"
```

---

*Architecture → [[02_Architecture_Globale]]*
*Docker → [[08_Docker_Infrastructure]]*
*Frontend → [[10_Frontend_Decision]]*
*JeryMotro AI → [[07_JeryMotro_AI_RAG]]*
