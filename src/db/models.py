"""ORM models.

Define your SQLAlchemy models here.
"""

from __future__ import annotations

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.orm.decl_api import DeclarativeBase
from sqlalchemy import Integer, String


class Base(DeclarativeBase):
    pass


class Example(Base):
    __tablename__ = "example"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)


