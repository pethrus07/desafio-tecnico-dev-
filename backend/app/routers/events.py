from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from .. import models, schemas
from ..database import get_db

router = APIRouter(prefix="/api", tags=["assets & events"])


@router.post("/assets", response_model=schemas.AssetOut, status_code=201)
def create_asset(payload: schemas.AssetCreate, db: Session = Depends(get_db)):
    asset = models.Asset(**payload.model_dump())
    db.add(asset)
    db.commit()
    db.refresh(asset)
    return asset


@router.get("/assets", response_model=list[schemas.AssetOut])
def list_assets(db: Session = Depends(get_db)):
    return db.query(models.Asset).all()


@router.post("/events", response_model=schemas.EventOut, status_code=201)
def create_event(payload: schemas.EventCreate, db: Session = Depends(get_db)):
    if not db.query(models.Asset).get(payload.asset_id):
        raise HTTPException(404, "Asset não encontrado")
    event = models.Event(**payload.model_dump())
    db.add(event)
    db.commit()
    db.refresh(event)
    return event


@router.get("/events", response_model=list[schemas.EventOut])
def list_events(asset_id: int | None = None, limit: int = 200, db: Session = Depends(get_db)):
    q = db.query(models.Event)
    if asset_id:
        q = q.filter(models.Event.asset_id == asset_id)
    return q.order_by(models.Event.timestamp.desc()).limit(limit).all()
