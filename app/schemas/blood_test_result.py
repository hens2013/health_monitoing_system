from pydantic import BaseModel
from datetime import date, datetime
from typing import Optional
import uuid

# Shared properties
class TestResultBase(BaseModel):
    user_id: int
    test_id: uuid.UUID
    test_date: date
    result_value: float

# Create Test Result
class TestResultCreate(TestResultBase):
    pass

# Update Test Result (Partial Update)
class TestResultUpdate(BaseModel):
    test_date: Optional[date]
    result_value: Optional[float]

# Test Result Response Schema
class TestResultResponse(TestResultBase):
    result_id: int
    created_at: datetime

    class Config:
        orm_mode = True
