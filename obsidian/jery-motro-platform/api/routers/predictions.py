from fastapi import APIRouter
from schemas.prediction import PredictionRequest, PredictionResponse
from services.madfirenet_service import MadFireNetService

router = APIRouter(prefix="/api/predictions", tags=["Prédictions ML"])

@router.post("/", response_model=PredictionResponse)
def predict_fire_risk(request: PredictionRequest):
    """
    Envoie les 18 features au modèle XGBoost (MadFireNet) et retourne le score de risque.
    """
    features_dict = request.model_dump()
    result = MadFireNetService.predict_risk(features_dict)
    return result
