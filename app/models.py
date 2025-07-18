from sqlalchemy import Column, Integer, String, DateTime, ARRAY, Boolean, ForeignKey, JSON, Text
from sqlalchemy.orm import relationship
import datetime
from .database import Base

#add logs table
class Log(Base):
    __tablename__ = "logs"
    id = Column(Integer, primary_key=True, index=True)

    type = Column(String, nullable=False)
    source_address = Column(String, nullable=False)
    source_port = Column(Integer, nullable=True)
    destination_address = Column(String, nullable=False)
    destination_host = Column(String, nullable=True)
    destination_port = Column(Integer, nullable=True)
    timestamp = Column(DateTime, nullable=False, default=datetime.datetime.utcnow)
    event_id = Column(String, nullable=True)
    logon_type = Column(String, nullable=True)
    logon_process = Column(String, nullable=True)
    username = Column(String, nullable=True)
    parent_process = Column(String, nullable=True)
    new_process = Column(String, nullable=True)
    creator_user = Column(String, nullable=True)
    url = Column(String, nullable=True)
    method = Column(String, nullable=True)
    user_agent = Column(String, nullable=True)
    http_response_status = Column(String, nullable=True)

class RawAlert(Base):
    __tablename__ = "raw_alerts"
    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow, nullable=True)
    source_ip = Column(String, nullable=False)
    destination_ip = Column(String, nullable=False)
    source_port = Column(Integer, nullable=True)
    destination_port = Column(Integer, nullable=True)
    source_hostname = Column(String, nullable=True)
    destination_hostname = Column(String, nullable=True)
    alert_type = Column(String, nullable=True)
    severity = Column(String, nullable=True)
    protocol = Column(String, nullable=True)
    firewall_action = Column(Boolean, nullable=True)
    rules_triggered = Column(ARRAY(String), nullable=True)
    trigger_reason = Column(String, nullable=True)
    analyzed = Column(Boolean, default=False)
    username = Column(String, nullable=True)
    user_agent = Column(String, nullable=True)
    http_request_method = Column(String, nullable=True)
    request_url = Column(String, nullable=True)

class Enrichment(Base):
    __tablename__ = "enrichments"
    id = Column(Integer, primary_key=True, index=True)
    alert_id = Column(Integer, ForeignKey("raw_alerts.id"))
    enrichment_type = Column(String)
    indicator_type = Column(String)
    indicator_value = Column(String)
    enrichment_result = Column(JSON)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
    
class AnalyzedAlert(Base):
    __tablename__ = "analyzed_alerts"

    id = Column(Integer, primary_key=True, index=True)
    alert_id = Column(Integer, ForeignKey("raw_alerts.id"), nullable=False, unique=True)
    isolation = Column(String, nullable=False)
    true_positive = Column(Boolean, nullable=False)
    attack_type = Column(String, nullable=False)
    severity = Column(String, nullable=False)
    recommendations = Column(Text, nullable=False)
    reasoning = Column(Text, nullable=False)
    artifacts_and_iocs = Column(JSON, nullable=True)
    summary = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    raw_alert = relationship("RawAlert", backref="analyzed_alert")

def __repr__(self):
    return f"<AnalyzedAlert(alert_id={self.alert_id}, severity={self.severity}, true_positive={self.true_positive})>"