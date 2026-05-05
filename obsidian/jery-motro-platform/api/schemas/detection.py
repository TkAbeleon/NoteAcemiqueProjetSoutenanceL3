from pydantic import BaseModel
from datetime import datetime

class DetectionResponse(BaseModel):
    id: int
    source: str
    latitude: float
    longitude: float
    acq_datetime: datetime
    frp: float
    confidence: str | None = None

    class Config:
        from_attributes = True
