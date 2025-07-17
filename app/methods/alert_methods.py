from app.database import SessionLocal
from app.models import RawAlert

def format_alert(alert):
    return (
        f"timestamp: {alert.timestamp}\n"
        f"source_ip: {alert.source_ip}\n"
        f"destination_ip: {alert.destination_ip}\n"
        f"source_port: {alert.source_port}\n"
        f"destination_port: {alert.destination_port}\n"
        f"source_hostname: {alert.source_hostname}\n"
        f"destination_hostname: {alert.destination_hostname}\n"
        f"alert_type: {alert.alert_type}\n"
        f"severity: {alert.severity}\n"
        f"rules_triggered: {alert.rules_triggered}\n"
        f"trigger_reason: {alert.trigger_reason}"
    )

def get_alert_from_db(alert_id):
    db = SessionLocal()
    alert = db.query(RawAlert).filter(RawAlert.id == alert_id).first()
    db.close()
    return alert
