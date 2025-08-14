from sqlalchemy import Column, Integer, String, Float, DateTime
from database import Base
from datetime import datetime

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)

class Rate(Base):
    __tablename__ = "rates"

    id = Column(Integer, primary_key=True, index=True)
    currency_pair = Column(String, index=True, nullable=False)  # e.g., USD-ZAR
    rate = Column(Float, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
