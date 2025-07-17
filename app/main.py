# app/main.py
from fastapi import FastAPI, HTTPException
from .database import engine, Base, SessionLocal
from .models import RawAlert, AnalyzedAlert
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session, class_mapper
from app.workflow import main as run_analysis

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Or restrict to ["http://localhost:3000"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)

@app.get("/")
def read_root():
    return {"message": "Hello from SOC_AI_AGENT backend!"}

@app.get("/alerts")
def get_alerts():
    db = SessionLocal()
    alerts = db.query(RawAlert).filter(RawAlert.analyzed == False).order_by(RawAlert.timestamp.desc()).all()
    db.close()
    return [alert.as_dict() for alert in alerts]

@app.get("/closed_alerts")
def get_closed_alerts():
    db = SessionLocal()
    analyzed = db.query(AnalyzedAlert).order_by(AnalyzedAlert.id.desc()).all()
    db.close()
    return [row.as_dict() for row in analyzed]

@app.get("/alerts/{alert_id}")
def get_alert_details(alert_id: int):
    db = SessionLocal()
    alert = db.query(RawAlert).filter(RawAlert.id == alert_id).first()
    db.close()
    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")
    return alert.as_dict()

@app.post("/alerts/{alert_id}/analyze")
def analyze_alert(alert_id: int):
    run_analysis(alert_id)
    return {"message": f"Alert {alert_id} analyzed."}

@app.post("/alerts/analyze_all")
def analyze_all_alerts():
    db = SessionLocal()
    alerts = db.query(RawAlert).filter(RawAlert.analyzed == False).all()
    db.close()
    ids = [a.id for a in alerts]
    for aid in ids:
        run_analysis(aid)
    return {"message": f"Analyzed {len(ids)} alerts."}


def as_dict(self):
    return {c.key: getattr(self, c.key) for c in class_mapper(self.__class__).columns}

RawAlert.as_dict = as_dict
AnalyzedAlert.as_dict = as_dict