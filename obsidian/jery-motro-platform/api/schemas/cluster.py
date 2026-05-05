from pydantic import BaseModel
from datetime import datetime

class ClusterResponse(BaseModel):
    id: int
    source: str
    latitude: float
    longitude: float
    acq_datetime: datetime
    frp: float

    class Config:
        from_attributes = True
