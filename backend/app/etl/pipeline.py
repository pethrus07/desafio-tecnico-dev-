"""Extract-transform-load dos eventos: agrega por ativo e gera alerta.

Lê tudo o que está em `events`, agrega numa passagem de pandas, apaga o
derivado antigo e regrava. É idempotente de propósito: rodar duas vezes dá
exatamente o mesmo banco, o que permite chamar o pipeline sem medo pelo botão
do dashboard. O julgamento de engenharia deste arquivo são os limiares fixos
abaixo; a parte estatística fica em `app/ml`.
"""
import pandas as pd
from sqlalchemy.orm import Session

from .. import models

# Limiares operacionais. Num cenário real viriam de config por ativo.
THRESHOLDS = {
    "temperature": 85.0,  # C
    "vibration": 7.0,     # mm/s
    "pressure": 12.0,     # bar
}


def _events_to_dataframe(db: Session) -> pd.DataFrame:
    # Traz a tabela inteira. É o preço da simplicidade e o primeiro ponto a
    # doer quando o histórico crescer — não há filtro de janela nem de ativo.
    rows = db.query(models.Event).all()
    if not rows:
        return pd.DataFrame()
    return pd.DataFrame(
        [
            {
                "asset_id": r.asset_id,
                "temperature": r.temperature,
                "vibration": r.vibration,
                "pressure": r.pressure,
                "runtime_hours": r.runtime_hours,
                "status": r.status,
            }
            for r in rows
        ]
    )


def run_etl(db: Session) -> dict:
    """Lê os eventos, agrega por ativo e grava métricas + alertas."""
    df = _events_to_dataframe(db)
    if df.empty:
        return {"processed_events": 0, "metrics": 0, "alerts": 0}

    # Agrega tudo numa passagem só.
    agg = (
        df.groupby("asset_id")
        .agg(
            avg_temperature=("temperature", "mean"),
            max_temperature=("temperature", "max"),
            avg_vibration=("vibration", "mean"),
            avg_pressure=("pressure", "mean"),
            # max, e não sum: runtime_hours é um contador acumulado do ativo.
            # Somar as leituras contaria as mesmas horas dezenas de vezes.
            total_runtime=("runtime_hours", "max"),
        )
        .reset_index()
    )

    # Recalcula do zero a cada run pra não duplicar (rodar 2x dá o mesmo resultado).
    # Cuidado: o delete de Alert leva junto os alertas de anomaly_model e de
    # failure_model, que não são deste pipeline. Por isso a ordem no
    # dashboard é ETL primeiro, modelos depois — invertida, o painel de
    # alertas perde tudo o que o ML tinha acabado de escrever.
    db.query(models.Metric).delete()
    db.query(models.Alert).delete()

    metrics_created = 0
    alerts_created = 0
    metric_names = ["avg_temperature", "max_temperature", "avg_vibration", "avg_pressure", "total_runtime"]

    for _, row in agg.iterrows():
        asset_id = int(row["asset_id"])

        for name in metric_names:
            db.add(models.Metric(asset_id=asset_id, name=name, value=float(row[name])))
            metrics_created += 1

        # Alertas por limiar
        if row["max_temperature"] > THRESHOLDS["temperature"]:
            db.add(models.Alert(
                asset_id=asset_id,
                severity="critical",
                message=f"Temperatura máxima {row['max_temperature']:.1f}C acima do limite.",
                source="threshold",
            ))
            alerts_created += 1

        if row["avg_vibration"] > THRESHOLDS["vibration"]:
            db.add(models.Alert(
                asset_id=asset_id,
                severity="warning",
                message=f"Vibração média {row['avg_vibration']:.2f} mm/s elevada.",
                source="threshold",
            ))
            alerts_created += 1

    db.commit()
    return {
        "processed_events": int(len(df)),
        "metrics": metrics_created,
        "alerts": alerts_created,
    }
