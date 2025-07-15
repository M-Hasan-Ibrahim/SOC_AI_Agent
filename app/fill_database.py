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
    skipped = 0

    for alert in alerts:
        if "timestamp" in alert and alert["timestamp"]:
            alert_dt = datetime.datetime.fromisoformat(alert["timestamp"])
        else:
            alert_dt = None

        existing = db.query(RawAlert).filter(
            and_(
                RawAlert.timestamp == alert_dt,
                RawAlert.alert_type == alert["alert_type"]
            )
        ).first()

        if existing:
            print(f"Skipping duplicate alert: {alert['alert_type']} at {alert['timestamp']}")
            skipped += 1
            continue

        alert["timestamp"] = alert_dt
        db_alert = RawAlert(**alert)
        db.add(db_alert)
        added += 1

    db.commit()
    db.close()
    print(f"Inserted {added} new alerts. Skipped {skipped} duplicates.")

if __name__ == "__main__":
    fill_database_from_json("app/sample_raw_alerts.json")
