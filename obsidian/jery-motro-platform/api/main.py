from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import engine, Base
from routers import detections, predictions, chat, clusters, alerts

# Initialisation des tables de la base de données
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="JeryMotro API", 
    description="API pour la détection et prédiction des feux de brousse à Madagascar",
    version="1.0.0"
)

# Configuration CORS pour autoriser le frontend (React/Vercel)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Enregistrement des routes
app.include_router(detections.router)
app.include_router(predictions.router)
app.include_router(chat.router)
app.include_router(clusters.router)
app.include_router(alerts.router)

@app.get("/api/health")
def health_check():
    return {"status": "ok", "system": "JeryMotro Platform Backend"}
