# schemas.py

from pydantic import BaseModel, EmailStr
from datetime import datetime


class RateResponse(BaseModel):
    id: int
    currency: str
    rate: float
    timestamp: datetime

    class Config:
        from_attributes = True 

class UserCreate(BaseModel):
    name: str
    username: str
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr

    class Config:
        orm_mode = True
