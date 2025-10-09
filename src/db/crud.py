"""CRUD helpers.

Add create/read/update/delete helpers for your models here.
"""

from __future__ import annotations

from typing import Optional

from sqlalchemy.orm import Session

from .models import Example


def create_example(db: Session, name: str) -> Example:
    example = Example(name=name)
    db.add(example)
    db.commit()
    db.refresh(example)
    return example


def get_example(db: Session, example_id: int) -> Optional[Example]:
    return db.get(Example, example_id)


