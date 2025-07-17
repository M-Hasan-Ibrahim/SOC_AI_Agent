import json
from sqlalchemy.orm import Session
from sqlalchemy import and_
from app.database import SessionLocal
from app.models import Log
import datetime

def fill_logs_from_json(json_file_path):
    with open(json_file_path, 'r') as f:
        logs = json.load(f)

    db: Session = SessionLocal()
    added = 0
    skipped = 0

    for log in logs:
        if "timestamp" in log and log["timestamp"]:
            log_dt = datetime.datetime.fromisoformat(log["timestamp"])
            log["timestamp"] = log_dt
        else:
            log["timestamp"] = None

        filters = []
        for col in Log.__table__.columns.keys():
            if col == "id":
                continue
            if col in log:
                filters.append(getattr(Log, col) == log[col])
            else:
                filters.append(getattr(Log, col) == None)

        existing = db.query(Log).filter(and_(*filters)).first()

        if existing:
            skipped += 1
            continue 
        else:
            db_log = Log(**log)
            db.add(db_log)
            added += 1

    db.commit()
    db.close()
    print(f"Inserted {added} new logs. Skipped {skipped} duplicates.")

if __name__ == "__main__":
    fill_logs_from_json("app/sample_logs.json")
