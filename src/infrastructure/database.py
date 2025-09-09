import os
from contextlib import suppress

from sqlalchemy import create_engine, text
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy_utils import create_database, database_exists

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+psycopg2://user:password@localhost:5432/embeddings_db")

engine = create_engine(DATABASE_URL)

# Crear DB si no existe (útil en dev)
if engine.url.host in ("localhost", "127.0.0.1") and not database_exists(engine.url):
    create_database(engine.url)

# Habilitar extensión pgvector al crear el esquema
# ruff: noqa: SIM117
with engine.connect() as conn:
    with suppress(Exception):
        conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector"))

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
