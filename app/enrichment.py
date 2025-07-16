import os
import requests

from app.models import Enrichment
from app.database import SessionLocal
import base64

#abuseipdb
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


def enrich_alert_ip_abuseipdb(alert_id, ip_address):
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

#virustotal_ip
def enrich_ip_with_virustotal(ip_address):
    api_key = os.environ.get("VIRUSTOTAL_API_KEY")
    url = f"https://www.virustotal.com/api/v3/ip_addresses/{ip_address}"
    headers = {
        "x-apikey": api_key
    }
    try:
        response = requests.get(url, headers=headers, timeout=15)
        return response.json()
    except Exception:
        return {"error": "Could not parse response"}

def enrich_alert_ip_virustotal(alert_id, ip_address):
    db = SessionLocal()
    result = enrich_ip_with_virustotal(ip_address)
    enrichment = Enrichment(
        alert_id=alert_id,
        enrichment_type='virustotal',
        indicator_type='ip',
        indicator_value=ip_address,
        enrichment_result=result
    )
    db.add(enrichment)
    db.commit()
    db.close()


#virustotal_url
def enrich_url_with_virustotal(url_to_check):
    api_key = os.environ.get("VIRUSTOTAL_API_KEY")
    api_url = "https://www.virustotal.com/api/v3/urls"
    headers = {
        "x-apikey": api_key
    }


    try:
        response = requests.post(api_url, headers=headers, data={"url": url_to_check}, timeout=15)
        response_json = response.json()
        if "data" in response_json and "id" in response_json["data"]:
            url_id = response_json["data"]["id"]
        else:
            return {"error": "Could not get URL ID from VirusTotal", "raw": response_json}

        report_url = f"{api_url}/{url_id}"
        report_response = requests.get(report_url, headers=headers, timeout=15)
        return report_response.json()
    except Exception as e:
        return {"error": f"Exception: {str(e)}"}

def enrich_alert_url_virustotal(alert_id, url_to_check):
    db = SessionLocal()
    result = enrich_url_with_virustotal(url_to_check)
    enrichment = Enrichment(
        alert_id=alert_id,
        enrichment_type='virustotal',
        indicator_type='url',
        indicator_value=url_to_check,
        enrichment_result=result
    )
    db.add(enrichment)
    db.commit()
    db.close()



#ipinfo
def enrich_ip_with_ipinfo(ip_address):
    api_key = os.environ.get("IPINFO_API_KEY")
    url = f"https://ipinfo.io/{ip_address}?token={api_key}"
    try:
        response = requests.get(url, timeout=10)
        return response.json()
    except Exception:
        return {"error": "Could not parse response"}

def enrich_alert_ip_ipinfo(alert_id, ip_address):
    db = SessionLocal()
    result = enrich_ip_with_ipinfo(ip_address)
    enrichment = Enrichment(
        alert_id=alert_id,
        enrichment_type='ipinfo.io',
        indicator_type='ip',
        indicator_value=ip_address,
        enrichment_result=result
    )
    db.add(enrichment)
    db.commit()
    db.close()
