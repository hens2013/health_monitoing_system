from pydantic import BaseModel
from datetime import datetime
from typing import Optional


# Shared properties
class ActivityBase(BaseModel):
    user_id: int
    activity_type_id: int
    start_time: datetime
    end_time: datetime
    calories_burned: Optional[float]
    avg_heart_rate: Optional[int]
    max_heart_rate: Optional[int]


# Create Activity Record
class ActivityCreate(ActivityBase):
    pass


# Update Activity Record (Partial Update)
class ActivityUpdate(BaseModel):
    start_time: Optional[datetime]
    end_time: Optional[datetime]
    calories_burned: Optional[float]
    avg_heart_rate: Optional[int]
    max_heart_rate: Optional[int]


# Activity Response Schema
class ActivityResponse(ActivityBase):
    activity_id: int
    duration: float
    created_at: datetime

    class Config:
        orm_mode = True
