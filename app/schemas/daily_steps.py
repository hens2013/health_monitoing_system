from pydantic import BaseModel
from datetime import date, datetime
from typing import Optional

# Shared properties
class StepsBase(BaseModel):
    user_id: int
    date: date
    total_steps: int
    total_calories_burned: Optional[float]
    distance_walked_km: Optional[float]
    active_minutes: Optional[int]

# Create Steps Record
class StepsCreate(StepsBase):
    pass

# Update Steps Record (Partial Update)
class StepsUpdate(BaseModel):
    total_steps: Optional[int]
    total_calories_burned: Optional[float]
    distance_walked_km: Optional[float]
    active_minutes: Optional[int]

# Steps Response Schema
class StepsResponse(StepsBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True
