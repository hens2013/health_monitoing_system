from pydantic import BaseModel, EmailStr
from datetime import date, datetime
from typing import Optional


# Shared properties
class UserBase(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    dob: date
    gender: str


# Create User
class UserCreate(UserBase):
    pass


# Update User (Partial Update)
class UserUpdate(BaseModel):
    first_name: Optional[str]
    last_name: Optional[str]
    email: Optional[EmailStr]
    dob: Optional[date]
    gender: Optional[str]


# User Response Schema
class UserResponse(UserBase):
    user_id: int
    created_at: datetime

    class Config:
        orm_mode = True
