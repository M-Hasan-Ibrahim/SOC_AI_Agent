from app.database import SessionLocal
from app.models import Log

def format_log_entry(log_obj):
    field_names = {
        "type": "Type",
        "source_address": "Source Address",
        "source_port": "Source Port",
        "destination_address": "Destination Address",
        "destination_host": "Destination Host",
        "destination_port": "Destination Port",
        "timestamp": "Timestamp",
        "event_id": "Event ID",
        "logon_type": "Logon Type",
        "logon_process": "Logon Process",
        "username": "Username",
        "parent_process": "Parent Process",
        "new_process": "New Process",
        "creator_user": "Creator User"
    }
    parts = []
    for key, label in field_names.items():
        value = getattr(log_obj, key, None)
        if value is not None and value != "" and value != 'null':
            parts.append(f"{label}: {value}")
    return "\n".join(parts)

def format_logs_for_prompt(logs):
    if not logs:
        return "No relevant logs found."
    result = []
    for idx, log in enumerate(logs, 1):
        result.append(f"Log #{idx}:\n{format_log_entry(log)}")
    return "\n\n".join(result)

def get_logs_for_alert_ips(source_ip, destination_ip):
    db = SessionLocal()
    logs = db.query(Log).filter((Log.source_address == source_ip) | (Log.destination_address == destination_ip)).all()
    db.close()
    return logs