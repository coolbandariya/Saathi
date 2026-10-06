from __future__ import annotations

import json
import logging
from contextvars import ContextVar
from time import perf_counter
from uuid import uuid4

_correlation_id: ContextVar[str | None] = ContextVar("saathi_correlation_id", default=None)
_logger = logging.getLogger("saathi")
_request_counts: dict[str, int] = {}
_request_latencies_ms: dict[str, list[float]] = {}


def new_correlation_id() -> str:
    return uuid4().hex


def set_correlation_id(value: str | None = None) -> str:
    correlation_id = value or new_correlation_id()
    _correlation_id.set(correlation_id)
    return correlation_id


def get_correlation_id() -> str | None:
    return _correlation_id.get()


def record_request(route: str, status_code: int, latency_ms: float) -> None:
    key = f"{route}:{status_code}"
    _request_counts[key] = _request_counts.get(key, 0) + 1
    samples = _request_latencies_ms.setdefault(route, [])
    samples.append(round(latency_ms, 2))
    if len(samples) > 200:
        del samples[:-200]


def metrics_snapshot() -> dict[str, object]:
    return {
        "requests": dict(_request_counts),
        "latency_ms": {
            route: {
                "count": len(values),
                "p50": _percentile(values, 0.50),
                "p95": _percentile(values, 0.95),
            }
            for route, values in _request_latencies_ms.items()
        },
    }


def _percentile(values: list[float], percentile: float) -> float:
    if not values:
        return 0.0
    ordered = sorted(values)
    index = min(len(ordered) - 1, max(0, round((len(ordered) - 1) * percentile)))
    return ordered[index]


def emit_event(event: str, **fields: object) -> None:
    payload = {
        "event": event,
        "correlation_id": get_correlation_id(),
        **fields,
    }
    _logger.info(json.dumps(payload, ensure_ascii=False, separators=(",", ":")))
