from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .database import Base, engine
from .routers import alerts, events, metrics

# Cria as tabelas no boot. Num projeto maior isso viraria migration (Alembic).
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Cortex Analytics Platform",
    description="Monitoramento operacional, ETL e métricas.",
    version="1.0.0",
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


@app.get("/", tags=["health"])
def root():
    return {"name": "Cortex Analytics Platform", "version": "1.0.0", "status": "online"}


@app.get("/health", tags=["health"])
def health():
    return {"status": "ok"}
