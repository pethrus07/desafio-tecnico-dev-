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
