import requests
from sqlalchemy.orm import Session
from models import Rate
from database import SessionLocal
from datetime import datetime

# Config
CURRENCIES = ["USD", "GBP", "ZAR"]
MARKUP = 0.10  # Additive markup

# Example free API URLs (replace with actual working ones)
API_URLS = [
    "https://api.exchangerate.host/latest?base=USD",
    "https://api.exchangerate-api.com/v4/latest/USD",
    "https://open.er-api.com/v6/latest/USD"
]

def fetch_rate_from_api(api_url, currency):
    try:
        resp = requests.get(api_url, timeout=5)
        resp.raise_for_status()
        data = resp.json()
        return data["rates"].get(currency)
    except Exception as e:
        print(f"Error fetching {currency} from {api_url}: {e}")
        return None

def aggregate_rate(currency: str):
    rates = [fetch_rate_from_api(url, currency) for url in API_URLS]
    # Filter out None values and calculate average
    valid_rates = [r for r in rates if r is not None]
    if not valid_rates:
        return None
    avg_rate = sum(valid_rates) / len(valid_rates)
    return round(avg_rate + MARKUP, 4)

def store_rate(currency: str, rate: float, db: Session):
    new_rate = Rate(currency=currency, rate=rate, timestamp=datetime.utcnow())
    db.add(new_rate)
    db.commit()
    db.refresh(new_rate)
    print(f"Stored {currency}: {rate}")
    return new_rate

def run_aggregation():
    db = SessionLocal()
    try:
        for currency in CURRENCIES:
            rate = aggregate_rate(currency)
            if rate is not None:
                store_rate(currency, rate, db)
    finally:
        db.close()
