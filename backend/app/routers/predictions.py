from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from .. import models, schemas
from ..database import get_db
from ..ml.anomaly import detect_anomalies
from ..ml.failure_prediction import predict_failures

router = APIRouter(prefix="/api/ml", tags=["machine learning"])


@router.post("/anomalies/run")
def run_anomaly_detection(db: Session = Depends(get_db)):
    return detect_anomalies(db)


@router.post("/failures/run")
def run_failure_prediction(db: Session = Depends(get_db)):
    return predict_failures(db)


@router.get("/predictions", response_model=list[schemas.PredictionOut])
def list_predictions(target: str | None = None, db: Session = Depends(get_db)):
    q = db.query(models.Prediction)
    if target:
        q = q.filter(models.Prediction.target == target)
    return q.order_by(models.Prediction.created_at.desc()).all()
