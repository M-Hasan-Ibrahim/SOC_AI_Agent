# app/main.py
from fastapi import FastAPI
from .database import engine, Base
from .models import RawAlert

app = FastAPI()

# Create tables on startup
@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)

@app.get("/")
def read_root():
    return {"message": "Hello from SOC_AI_AGENT backend!"}
