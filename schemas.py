from pydantic import BaseModel
from datetime import datetime

# User schemas
class UserCreate(BaseModel):
    name: str
    email: str
    password: str

class UserResponse(BaseModel):
    id: int
    name: str
    email: str

    class Config:
        orm_mode = True

# Rate schemas
class RateResponse(BaseModel):
    currency_pair: str
    rate: float
    timestamp: datetime

    class Config:
        orm_mode = True
