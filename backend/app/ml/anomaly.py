import pandas as pd
from sklearn.ensemble import IsolationForest
from sqlalchemy.orm import Session

from .. import models

FEATURES = ["temperature", "vibration", "pressure"]


def detect_anomalies(db: Session, contamination: float = 0.08) -> dict:
    """Detecta leituras fora do padrão com Isolation Forest.

    Usei Isolation Forest porque é não-supervisionado: não preciso de
    rótulos de falha, só isolar o que destoa do comportamento normal.
    """
    rows = db.query(models.Event).all()
    if len(rows) < 10:
        return {"trained": False, "reason": "poucos dados (mínimo 10 eventos)"}

    df = pd.DataFrame(
        [{**{f: getattr(r, f) for f in FEATURES}, "asset_id": r.asset_id} for r in rows]
    )

    model = IsolationForest(n_estimators=150, contamination=contamination, random_state=42)
    df["anomaly"] = model.fit_predict(df[FEATURES])  # -1 = anômalo, 1 = normal

    db.query(models.Prediction).filter(models.Prediction.target == "anomaly").delete()

    # Por ativo: qual a fração de leituras anômalas.
    summary = (
        df.groupby("asset_id")
        .agg(anomaly_rate=("anomaly", lambda s: float((s == -1).mean())))
        .reset_index()
    )

    scored = 0
    for _, row in summary.iterrows():
        rate = float(row["anomaly_rate"])
        label = "anomalous" if rate > 0.15 else "normal"

        db.add(models.Prediction(
            asset_id=int(row["asset_id"]),
            model="isolation_forest",
            target="anomaly",
            score=round(rate, 4),
            label=label,
        ))

        if label == "anomalous":
            db.add(models.Alert(
                asset_id=int(row["asset_id"]),
                severity="warning",
                message=f"Comportamento anômalo detectado ({rate:.0%} das leituras).",
                source="anomaly_model",
            ))
        scored += 1

    db.commit()
    return {"trained": True, "assets_scored": scored}
