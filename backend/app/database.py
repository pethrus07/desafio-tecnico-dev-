"""Conexão com o banco: engine, sessão e a dependência `get_db`.

Um arquivo só decide onde os dados moram. `DATABASE_URL` escolhe entre
Postgres (o que o docker-compose sobe) e um SQLite em arquivo, que é o padrão
para o projeto rodar sem subir nada. Todo router recebe a sessão por
`Depends(get_db)` — ninguém abre sessão por conta própria, e é isso que
garante que a sessão sempre feche, mesmo se a rota levantar exceção.
"""
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# Em produção usamos Postgres (via DATABASE_URL). Sem essa variável,
# cai no SQLite local pra facilitar rodar o projeto sem subir banco.
# Atenção: ninguém lê o arquivo .env. `python-dotenv` está no requirements
# mas não é importado em lugar nenhum, então a variável tem de vir do
# ambiente de verdade (é o docker-compose que a injeta). Se não vier, o
# SQLite assume em silêncio — e um "banco vazio" costuma ser isto.
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./cortex.db")

# check_same_thread=False porque o driver do SQLite recusa usar a conexão
# em outra thread, e o FastAPI roda rota síncrona num pool de threads.
connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}

# pool_pre_ping testa a conexão antes de entregá-la: Postgres em container
# derruba conexão ociosa, e sem isso o primeiro request depois da pausa morre.
engine = create_engine(DATABASE_URL, connect_args=connect_args, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
