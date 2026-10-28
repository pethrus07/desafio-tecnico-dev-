"""Leitura dos alertas. Só leitura.

Alerta não nasce de requisição: quem escreve é o ETL (por limiar) e os dois
modelos de ML. Esta rota existe para o painel do dashboard, e ordena do mais
recente para o mais antigo porque é assim que o painel mostra.
"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from .. import models, schemas
from ..database import get_db

router = APIRouter(prefix="/api", tags=["alerts"])


@router.get("/alerts", response_model=list[schemas.AlertOut])
def list_alerts(severity: str | None = None, db: Session = Depends(get_db)):
    q = db.query(models.Alert)
    if severity:
        q = q.filter(models.Alert.severity == severity)
    return q.order_by(models.Alert.created_at.desc()).all()
