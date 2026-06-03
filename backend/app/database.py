import os

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# Em produção usamos Postgres (via DATABASE_URL). Sem essa variável,
# cai no SQLite local pra facilitar rodar o projeto sem subir banco.
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./cortex.db")

connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}

engine = create_engine(DATABASE_URL, connect_args=connect_args, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
