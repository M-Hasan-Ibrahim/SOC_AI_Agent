from app.models import Enrichment
import json
from app.database import SessionLocal


def format_enrichment(enrichment_obj):
    if enrichment_obj is None:
        return "No enrichment data available."
    return (
        f"Tool used: {enrichment_obj.enrichment_type}\n"
        f"Indicator: {enrichment_obj.indicator_type}: {enrichment_obj.indicator_value}\n"
        f"Enrichment result: {json.dumps(enrichment_obj.enrichment_result, indent=2)}"
    )
    
def format_multiple_enrichments(enrichments):
    if not enrichments:
        return "No enrichment data available."
    text = ""
    for enrichment in enrichments:
        text += (
            f"Tool used: {enrichment.enrichment_type}\n"
            f"Indicator: {enrichment.indicator_type}: {enrichment.indicator_value}\n"
            f"Enrichment result: {json.dumps(enrichment.enrichment_result, indent=2)}\n\n"
        )
    return text.strip()

def get_all_enrichment_for_alert(alert_id):
    db = SessionLocal()
    enrichment_obj = db.query(Enrichment).filter(Enrichment.alert_id == alert_id).all()
    db.close()
    return enrichment_obj

def get_enrichment(alert_id, tool_name, indicator_type="ip", indicator_value=None):
    db = SessionLocal()
    query = db.query(Enrichment).filter(
        Enrichment.alert_id == alert_id,
        Enrichment.enrichment_type.ilike(tool_name),
        Enrichment.indicator_type == indicator_type
    )
    if indicator_value:
        query = query.filter(Enrichment.indicator_value == indicator_value)
    enrichment = query.first()
    db.close()
    return enrichment