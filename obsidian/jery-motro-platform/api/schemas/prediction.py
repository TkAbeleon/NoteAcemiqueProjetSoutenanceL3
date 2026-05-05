from pydantic import BaseModel

class PredictionRequest(BaseModel):
    frp: float
    diff_brightness: float
    local_hour: int
    is_dry_season: int
    cluster_size: int
    temperature_2m: float
    slope_deg: float
    ndvi_10m: float

class PredictionResponse(BaseModel):
    risk_score: float
    niveau_risque: str
    model_version: str
