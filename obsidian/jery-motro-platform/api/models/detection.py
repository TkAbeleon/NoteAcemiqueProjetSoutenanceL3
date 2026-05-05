from sqlalchemy import Column, Integer, Float, String, DateTime
from database import Base

class Detection(Base):
    __tablename__ = "firms_fire_detections"

    id = Column(Integer, primary_key=True, index=True)
    source = Column(String(30))
    latitude = Column(Float)
    longitude = Column(Float)
    acq_datetime = Column(DateTime)
    frp = Column(Float)
    confidence = Column(String(10))
