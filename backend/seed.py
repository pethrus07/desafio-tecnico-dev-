"""Popula o banco com dados sintéticos pra demonstração.

Gera ativos saudáveis e alguns "doentes" (com piora ao longo do tempo e
eventos de falha), assim os modelos de ML têm sinal pra aprender.

    python seed.py
"""
import random
from datetime import datetime, timedelta

from app.database import Base, SessionLocal, engine
from app import models

random.seed(42)

ASSETS = [
    {"name": "Compressor A", "type": "compressor", "location": "Planta 1", "healthy": True},
    {"name": "Bomba Hidráulica B", "type": "pump", "location": "Planta 1", "healthy": True},
    {"name": "Motor C", "type": "motor", "location": "Planta 2", "healthy": False},
    {"name": "Turbina D", "type": "turbine", "location": "Planta 2", "healthy": False},
    {"name": "Esteira E", "type": "conveyor", "location": "Planta 3", "healthy": True},
]


def generate():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    now = datetime.utcnow()

    for spec in ASSETS:
        asset = models.Asset(name=spec["name"], type=spec["type"], location=spec["location"])
        db.add(asset)
        db.flush()  # precisa do asset.id antes de criar os eventos

        runtime = random.uniform(1000, 5000)
        for i in range(60):
            runtime += random.uniform(0.5, 2.0)

            if spec["healthy"]:
                temp = random.gauss(70, 5)
                vib = random.gauss(4.0, 0.8)
                press = random.gauss(9.0, 0.6)
                status = "ok"
            else:
                drift = i / 60  # vai piorando com o tempo
                temp = random.gauss(78 + drift * 18, 4)
                vib = random.gauss(5.0 + drift * 4, 1.0)
                press = random.gauss(10.0 + drift * 2, 0.8)
                if temp > 92 or vib > 9:
                    status = "down"
                elif temp > 85 or vib > 7:
                    status = "warning"
                else:
                    status = "ok"

            db.add(models.Event(
                asset_id=asset.id,
                temperature=round(temp, 2),
                vibration=round(vib, 2),
                pressure=round(press, 2),
                runtime_hours=round(runtime, 1),
                status=status,
                timestamp=now - timedelta(hours=(60 - i)),
            ))

    db.commit()
    print(f"Seed ok: {db.query(models.Asset).count()} ativos, {db.query(models.Event).count()} eventos")
    db.close()


if __name__ == "__main__":
    generate()
