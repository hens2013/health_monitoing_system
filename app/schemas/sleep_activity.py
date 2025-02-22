from pydantic import BaseModel
from datetime import date, datetime
from typing import Optional

# Shared properties
class SleepBase(BaseModel):
    user_id: int
    sleep_date: date
    sleep_duration: int
    sleep_efficiency: float
    deep_sleep_min: int
    rem_sleep_min: int
    wakeups: int
    bedtime: datetime
    wake_time: datetime

# Create Sleep Record
class SleepCreate(SleepBase):
    pass

# Update Sleep Record (Partial Update)
class SleepUpdate(BaseModel):
    sleep_duration: Optional[int]
    sleep_efficiency: Optional[float]
    deep_sleep_min: Optional[int]
    rem_sleep_min: Optional[int]
    wakeups: Optional[int]
    bedtime: Optional[datetime]
    wake_time: Optional[datetime]

# Sleep Response Schema
class SleepResponse(SleepBase):
    sleep_id: int
    created_at: datetime

    class Config:
        orm_mode = True
