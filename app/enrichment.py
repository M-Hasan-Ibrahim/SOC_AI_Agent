import os
import requests

from app.models import Enrichment
from app.database import SessionLocal

def enrich_ip_with_abuseipdb(ip_address):
    api_key = os.environ.get("ABUSEIPDB_API_KEY")
    url = "https://api.abuseipdb.com/api/v2/check"
    headers = {
        "Accept": "application/json",
        "Key": api_key
    }
    params = {
        "ipAddress": ip_address,
        "maxAgeInDays": 90
    }
    response = requests.get(url, headers=headers, params=params)
    try:
        return response.json()
    except Exception:
        return {"error": "Could not parse response"}


def enrich_alert_ip(alert_id, ip_address):
    db = SessionLocal()
    result = enrich_ip_with_abuseipdb(ip_address)
    enrichment = Enrichment(
        alert_id=alert_id,
        enrichment_type='abuseipdb',
        indicator_type='ip',
        indicator_value=ip_address,
        enrichment_result=result
    )
    db.add(enrichment)
    db.commit()
    db.close()