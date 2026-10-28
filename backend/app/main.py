"""Entrada da API: monta o FastAPI, o CORS e os quatro routers.

Único arquivo que conhece todos os routers, e único lugar onde as tabelas
nascem: o projeto não tem migrations, então o banco só existe por causa do
`create_all` abaixo (ou do `seed.py`, que derruba e recria tudo).
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .database import Base, engine
from .routers import alerts, events, metrics, predictions

# Cria as tabelas no boot. Num projeto maior isso viraria migration (Alembic).
# create_all só CRIA o que falta: não altera coluna de tabela existente.
# Mexeu em models.py com banco já populado, o jeito é apagar o .db e semear
# de novo — é a contrapartida de não ter migrations.
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Cortex Analytics Platform",
    description="Monitoramento operacional, ETL e modelos de ML para análise preditiva.",
    version="2.0.0",
)

# CORS liberado pra facilitar o dev. Em produção, restringir ao domínio do front.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(events.router)
app.include_router(metrics.router)
app.include_router(alerts.router)
app.include_router(predictions.router)


@app.get("/", tags=["health"])
def root():
    return {"name": "Cortex Analytics Platform", "version": "2.0.0", "status": "online"}


@app.get("/health", tags=["health"])
def health():
    return {"status": "ok"}
