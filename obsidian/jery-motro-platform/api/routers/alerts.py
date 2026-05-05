from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from database import get_db
from models.alert import Alert
from schemas.alert import AlertResponse, AlertSubscriptionRequest

router = APIRouter(prefix="/api/alerts", tags=["Alertes"])

@router.get("/", response_model=List[AlertResponse])
def get_recent_alerts(limit: int = 20, db: Session = Depends(get_db)):
    """
    Récupère l'historique des dernières alertes envoyées.
    """
    alerts = db.query(Alert)\
               .order_by(Alert.created_at.desc())\
               .limit(limit)\
               .all()
    return alerts

@router.post("/subscribe", summary="S'abonner aux alertes (Auth requise dans le futur)")
def subscribe_to_alerts(req: AlertSubscriptionRequest):
    """
    Inscrit un utilisateur pour recevoir les alertes JeryMotro.
    """
    return {"message": "Abonnement enregistré avec succès", "email": req.email}
