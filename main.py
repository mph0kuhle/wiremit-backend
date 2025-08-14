from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from database import Base, engine
from auth import router as auth_router
from rate_aggregator import run_aggregation
from apscheduler.schedulers.background import BackgroundScheduler
from database import get_db
from models import Rate

Base.metadata.create_all(bind=engine)
app = FastAPI(title="Wiremit Forex Aggregator Backend")
app.include_router(auth_router)

@app.get("/rates")
def get_all_rates(db: Session = Depends(get_db)):
    rates = db.query(Rate).all()
    return [{"currency": r.currency, "rate": r.rate, "timestamp": r.timestamp} for r in rates]

@app.get("/rates/{currency}")
def get_rate(currency: str, db: Session = Depends(get_db)):
    rate = db.query(Rate).filter(Rate.currency.ilike(currency)).first()
    if not rate:
        raise HTTPException(status_code=404, detail="Currency not found")
    return {"currency": rate.currency, "rate": rate.rate, "timestamp": rate.timestamp}

@app.get("/historical/rates")
def get_historical_rates(db: Session = Depends(get_db)):
    rates = db.query(Rate).order_by(Rate.timestamp.desc()).all()
    return [{"currency": r.currency, "rate": r.rate, "timestamp": r.timestamp} for r in rates]

@app.get("/")
def root():
    return {"message": "Wiremit Backend API running"}

scheduler = BackgroundScheduler()
scheduler.add_job(run_aggregation, "interval", hours=1)
scheduler.start()

@app.on_event("startup")
def startup_event():
    run_aggregation()

from rate_routes import router as rate_router
app.include_router(rate_router)
