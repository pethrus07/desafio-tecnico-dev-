from datetime import datetime

from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .database import Base

# Domínio: monitoramento de ativos (máquinas/sensores).
# Asset -> tem vários Event (leituras). Metric e Alert são derivados gerados pelo ETL.


class Asset(Base):
    __tablename__ = "assets"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    type = Column(String, nullable=False, default="machine")
    location = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    events = relationship("Event", back_populates="asset", cascade="all, delete-orphan")


class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True)
    asset_id = Column(Integer, ForeignKey("assets.id"), index=True)
    temperature = Column(Float, nullable=False)
    vibration = Column(Float, nullable=False)
    pressure = Column(Float, nullable=False)
    runtime_hours = Column(Float, nullable=False, default=0.0)
    status = Column(String, default="ok")  # ok | warning | down
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)

    asset = relationship("Asset", back_populates="events")


class Metric(Base):
    __tablename__ = "metrics"

    id = Column(Integer, primary_key=True, index=True)
    asset_id = Column(Integer, ForeignKey("assets.id"), index=True)
    name = Column(String, nullable=False)
    value = Column(Float, nullable=False)
    window = Column(String, default="all")
    computed_at = Column(DateTime, default=datetime.utcnow)


class Alert(Base):
    __tablename__ = "alerts"

    id = Column(Integer, primary_key=True, index=True)
    asset_id = Column(Integer, ForeignKey("assets.id"), index=True)
    severity = Column(String, default="warning")  # info | warning | critical
    message = Column(String, nullable=False)
    source = Column(String, default="threshold")  # threshold | anomaly_model | failure_model
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
