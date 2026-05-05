from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from database import get_db
from models.detection import Detection
from schemas.detection import DetectionResponse

router = APIRouter(prefix="/api/detections", tags=["Detections"])

@router.get("/", response_model=List[DetectionResponse])
def get_recent_detections(limit: int = 50, min_frp: float = 0.0, db: Session = Depends(get_db)):
    """
    Récupère les dernières détections de feux.
    Filtre optionnel par niveau de FRP minimum.
    """
    feux = db.query(Detection)\
             .filter(Detection.frp >= min_frp)\
             .order_by(Detection.acq_datetime.desc())\
             .limit(limit)\
             .all()
    return feux
