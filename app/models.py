# app/models.py
from sqlalchemy import Column, Integer, String, DateTime, ARRAY, Boolean
import datetime
from .database import Base

class RawAlert(Base):
    __tablename__ = "raw_alerts"
    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow, nullable=True)
    source_ip = Column(String, nullable=True)
    destination_ip = Column(String, nullable=True)
    source_port = Column(Integer, nullable=True)
    destination_port = Column(Integer, nullable=True)
    source_hostname = Column(String, nullable=True)
    destination_hostname = Column(String, nullable=True)
    alert_type = Column(String, nullable=True)
    severity = Column(String, nullable=True)
    rules_triggered = Column(ARRAY(String), nullable=True)
    trigger_reason = Column(String, nullable=True)
    analyzed = Column(Boolean, default=False)
