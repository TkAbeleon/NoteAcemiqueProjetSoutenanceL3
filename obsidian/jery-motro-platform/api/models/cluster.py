from sqlalchemy import Column, Integer, Float, String, DateTime
from database import Base

class Cluster(Base):
    __tablename__ = "firms_hotspots" # J'utilise cette table comme proxy des clusters pour le prototype

    id = Column(Integer, primary_key=True, index=True)
    source = Column(String(30))
    latitude = Column(Float)
    longitude = Column(Float)
    acq_datetime = Column(DateTime)
    frp = Column(Float)
