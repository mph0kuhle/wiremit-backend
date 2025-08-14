from fastapi import FastAPI
from database import Base, engine

# Import models to ensure tables are created
import models

app = FastAPI(title="Wiremit Forex Aggregator Backend")

# Create DB tables
Base.metadata.create_all(bind=engine)

@app.get("/")
def root():
    return {"message": "Wiremit Backend API running"}
