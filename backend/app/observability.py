from __future__ import annotations

from contextvars import ContextVar
from uuid import uuid4

_correlation_id: ContextVar[str | None] = ContextVar("saathi_correlation_id", default=None)


def new_correlation_id() -> str:
    return uuid4().hex


def set_correlation_id(value: str | None = None) -> str:
    correlation_id = value or new_correlation_id()
    _correlation_id.set(correlation_id)
    return correlation_id


def get_correlation_id() -> str | None:
    return _correlation_id.get()
