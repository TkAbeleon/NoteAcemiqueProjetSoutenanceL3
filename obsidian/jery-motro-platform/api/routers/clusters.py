from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from database import get_db
from models.cluster import Cluster
from schemas.cluster import ClusterResponse

router = APIRouter(prefix="/api/clusters", tags=["Clusters"])

@router.get("/", response_model=List[ClusterResponse])
def get_recent_clusters(limit: int = 20, db: Session = Depends(get_db)):
    """
    Récupère les derniers clusters actifs.
    Basé sur la vue firms_hotspots (FRP > 50).
    """
    clusters = db.query(Cluster)\
                 .order_by(Cluster.acq_datetime.desc())\
                 .limit(limit)\
                 .all()
    return clusters
