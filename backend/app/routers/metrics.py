from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from .. import models, schemas
from ..database import get_db
from ..etl.pipeline import run_etl

router = APIRouter(prefix="/api", tags=["metrics & etl"])


@router.post("/etl/run")
def trigger_etl(db: Session = Depends(get_db)):
    return run_etl(db)


@router.get("/metrics", response_model=list[schemas.MetricOut])
def list_metrics(asset_id: int | None = None, db: Session = Depends(get_db)):
    q = db.query(models.Metric)
    if asset_id:
        q = q.filter(models.Metric.asset_id == asset_id)
    return q.all()


@router.get("/dashboard/summary", response_model=schemas.KPISummary)
def dashboard_summary(db: Session = Depends(get_db)):
    total_assets = db.query(models.Asset).count()
    total_events = db.query(models.Event).count()
    open_alerts = db.query(models.Alert).count()

    events = db.query(models.Event).all()
    if events:
        avg_temp = sum(e.temperature for e in events) / len(events)
        avg_vib = sum(e.vibration for e in events) / len(events)
        # uptime = % de leituras com status ok
        uptime = sum(1 for e in events if e.status == "ok") / len(events) * 100
    else:
        avg_temp = avg_vib = uptime = 0.0

    return schemas.KPISummary(
        total_assets=total_assets,
        total_events=total_events,
        open_alerts=open_alerts,
        avg_temperature=round(avg_temp, 2),
        avg_vibration=round(avg_vib, 2),
        uptime_pct=round(uptime, 1),
    )
