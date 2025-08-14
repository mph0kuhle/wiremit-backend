from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime

from database import get_db
from models import Rate
from schemas import RateResponse

router = APIRouter()

#All currency
@router.get("/rates", response_model=List[RateResponse])
def get_latest_rates(db: Session = Depends(get_db)):
    subquery = db.query(
        Rate.currency,
        Rate.rate,
        Rate.timestamp
    ).from_statement(
        """
        SELECT r1.id, r1.currency, r1.rate, r1.timestamp
        FROM rates r1
        INNER JOIN (
            SELECT currency, MAX(timestamp) as max_time
            FROM rates
            GROUP BY currency
        ) r2
        ON r1.currency = r2.currency AND r1.timestamp = r2.max_time
        """
    ).all()
    return subquery

# Latest rate
@router.get("/rates/{currency}", response_model=RateResponse)
def get_rate(currency: str, db: Session = Depends(get_db)):
    rate = (
        db.query(Rate)
        .filter(Rate.currency == currency.upper())
        .order_by(Rate.timestamp.desc())
        .first()
    )
    if not rate:
        raise HTTPException(status_code=404, detail="Currency rate not found")
    return rate

#Past rates
@router.get("/historical/rates/{currency}", response_model=List[RateResponse])
def get_historical_rates(currency: str, db: Session = Depends(get_db)):
    rates = (
        db.query(Rate)
        .filter(Rate.currency == currency.upper())
        .order_by(Rate.timestamp.desc())
        .all()
    )
    if not rates:
        raise HTTPException(status_code=404, detail="No historical rates found")
    return rates
