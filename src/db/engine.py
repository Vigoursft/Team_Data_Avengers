"""Database engine and session setup.

Adjust the DATABASE_URL in src/config.py or environment variables as needed.
"""

from __future__ import annotations

import os
from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


def get_database_url() -> str:
    # Prefer env var; fallback to src.config if present; final fallback is SQLite file
    db_url = os.getenv("DATABASE_URL")
    if db_url:
        return db_url
    try:
        from src.config import DATABASE_URL  # type: ignore

        if DATABASE_URL:
            return str(DATABASE_URL)
    except Exception:
        pass
    return "sqlite:///./app.db"


ENGINE = create_engine(get_database_url(), future=True)
SessionLocal = sessionmaker(bind=ENGINE, autocommit=False, autoflush=False, future=True)


def get_session() -> Generator:
    """Yield a SQLAlchemy session, closing it afterwards."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


