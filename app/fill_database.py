import json
from sqlalchemy.orm import Session
from sqlalchemy import and_
from app.database import SessionLocal
from app.models import RawAlert
import datetime

def fill_database_from_json(json_file_path):
    with open(json_file_path, 'r') as f:
        alerts = json.load(f)

    db: Session = SessionLocal()
    added = 0
    updated = 0

    for alert in alerts:
        if "timestamp" in alert and alert["timestamp"]:
            alert_dt = datetime.datetime.fromisoformat(alert["timestamp"])
        else:
            alert_dt = None

        existing = db.query(RawAlert).filter(
            and_(
                RawAlert.timestamp == alert_dt,
                RawAlert.alert_type == alert["alert_type"],
                RawAlert.source_ip == alert["source_ip"],
                RawAlert.destination_ip == alert["destination_ip"]
            )
        ).first()
        
        alert["timestamp"] = alert_dt

        if existing:
            for key in RawAlert.__table__.columns.keys():
                if key == "id":
                    continue
                if key in alert:
                    setattr(existing, key, alert[key])
                else:
                    setattr(existing, key, None)
            updated += 1
        else:
            db_alert = RawAlert(**alert)
            db.add(db_alert)
            added += 1
                
    db.commit()
    db.close()
    print(f"Inserted {added} new alerts. Updated {updated} alerts.")

if __name__ == "__main__":
    fill_database_from_json("app/sample_raw_alerts.json")
