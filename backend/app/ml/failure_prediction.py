"""Risco de falha por Random Forest, agregado por ativo.

Aprende a assinatura de sensor de uma leitura marcada `down` e devolve, por
ativo, a probabilidade média de as leituras dele se parecerem com isso.
Cuidado com a leitura do número: é um retrato do histórico, não uma previsão
do futuro — o porquê está no comentário do treino e na seção 6 de
`docs/ARQUITETURA.md`.
"""
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sqlalchemy.orm import Session

from .. import models

FEATURES = ["temperature", "vibration", "pressure", "runtime_hours"]


def predict_failures(db: Session) -> dict:
    """Estima o risco de falha de cada ativo com Random Forest.

    O rótulo de falha vem do histórico (status == 'down'). Escolhi Random
    Forest pela robustez e por dar a importância das features de graça,
    o que ajuda a explicar o resultado pro time de operação.
    """
    rows = db.query(models.Event).all()
    if len(rows) < 20:
        return {"trained": False, "reason": "poucos dados (mínimo 20 eventos)"}

    df = pd.DataFrame(
        [
            {
                **{f: getattr(r, f) for f in FEATURES},
                "asset_id": r.asset_id,
                "failed": 1 if r.status == "down" else 0,
            }
            for r in rows
        ]
    )

    # Sem as duas classes (falhou / não falhou) não dá pra treinar.
    if df["failed"].nunique() < 2:
        return {"trained": False, "reason": "sem variabilidade de classes no histórico"}

    # Duas ressalvas que mudam como o número deve ser lido:
    # 1) treino e escore saem das MESMAS linhas, sem conjunto de teste — a
    #    probabilidade é o modelo reconhecendo o histórico, não generalizando;
    # 2) `failed` é o status da própria leitura, não uma falha que veio depois
    #    dela, então o que sai daqui classifica o estado presente do ativo.
    # Para virar previsão de verdade, o rótulo teria de olhar uma janela à
    # frente do evento (por exemplo: "houve down nas próximas 24h?").
    model = RandomForestClassifier(
        n_estimators=200, max_depth=8, class_weight="balanced", random_state=42
    )
    model.fit(df[FEATURES], df["failed"])
    df["risk"] = model.predict_proba(df[FEATURES])[:, 1]

    db.query(models.Prediction).filter(models.Prediction.target == "failure_risk").delete()

    summary = df.groupby("asset_id").agg(risk=("risk", "mean")).reset_index()

    scored = 0
    for _, row in summary.iterrows():
        risk = float(row["risk"])
        if risk >= 0.66:
            label = "high_risk"
        elif risk >= 0.33:
            label = "medium_risk"
        else:
            label = "low_risk"

        db.add(models.Prediction(
            asset_id=int(row["asset_id"]),
            model="random_forest",
            target="failure_risk",
            score=round(risk, 4),
            label=label,
        ))

        if label == "high_risk":
            db.add(models.Alert(
                asset_id=int(row["asset_id"]),
                severity="critical",
                message=f"Alto risco de falha previsto ({risk:.0%}).",
                source="failure_model",
            ))
        scored += 1

    db.commit()

    importances = {f: round(float(v), 3) for f, v in zip(FEATURES, model.feature_importances_)}
    return {"trained": True, "assets_scored": scored, "feature_importances": importances}
