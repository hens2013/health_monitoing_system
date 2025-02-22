from pydantic import BaseModel
from typing import Optional
import uuid

# Shared properties
class TestBase(BaseModel):
    test_name: str
    unit: str
    lower_bound: Optional[float]
    upper_bound: Optional[float]

# Create Test
class TestCreate(TestBase):
    pass

# Update Test (Partial Update)
class TestUpdate(BaseModel):
    test_name: Optional[str]
    unit: Optional[str]
    lower_bound: Optional[float]
    upper_bound: Optional[float]

# Test Response Schema
class TestResponse(TestBase):
    test_id: uuid.UUID

    class Config:
        orm_mode = True
