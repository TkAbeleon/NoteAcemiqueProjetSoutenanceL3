from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    
    class Config:
        from_attributes = True

class AlertResponse(BaseModel):
    id: int
    message: str
    status: str
    sent_at: Optional[datetime] = None
    created_at: datetime
    user: Optional[UserResponse] = None

    class Config:
        from_attributes = True

class AlertSubscriptionRequest(BaseModel):
    email: str
    phone_number: Optional[str] = None
    region_preference: Optional[str] = None
