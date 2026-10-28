"""Os contratos de entrada e saída da API (Pydantic v2).

Existem separados de `models.py` justamente para a resposta não ser o espelho
da tabela e para a entrada não aceitar campo que é do servidor (`id`,
`created_at`, `timestamp`). `from_attributes=True` é o que deixa o FastAPI
serializar o objeto do ORM direto, sem conversão à mão.
"""
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class AssetBase(BaseModel):
    name: str
    type: str = "machine"
    location: Optional[str] = None


class AssetCreate(AssetBase):
    pass


class AssetOut(AssetBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    created_at: datetime


class EventBase(BaseModel):
    asset_id: int
    temperature: float
    vibration: float
    pressure: float
    runtime_hours: float = 0.0
    status: str = "ok"


class EventCreate(EventBase):
    pass


class EventOut(EventBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    timestamp: datetime


class MetricOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    asset_id: int
    name: str
    value: float
    window: str
    computed_at: datetime


class AlertOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    asset_id: int
    severity: str
    message: str
    source: str
    created_at: datetime


class PredictionOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    asset_id: int
    model: str
    target: str
    score: float
    label: str
    created_at: datetime


# Resposta agregada usada nos KPIs do topo do dashboard.
class KPISummary(BaseModel):
    total_assets: int
    total_events: int
    open_alerts: int
    avg_temperature: float
    avg_vibration: float
    uptime_pct: float
