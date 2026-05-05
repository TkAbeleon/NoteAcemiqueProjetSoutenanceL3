from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100))
    email = Column(String(255), unique=True)
    phone = Column(String(20))
    created_at = Column(DateTime)
    
    alerts = relationship("Alert", back_populates="user")

class Alert(Base):
    __tablename__ = "alerts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    detection_id = Column(Integer, ForeignKey("firms_fire_detections.id"))
    message = Column(String)
    status = Column(String(20))
    sent_at = Column(DateTime)
    created_at = Column(DateTime)

    user = relationship("User", back_populates="alerts")
