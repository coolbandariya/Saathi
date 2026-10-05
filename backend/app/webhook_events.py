from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
from threading import Lock
from typing import Protocol


class WebhookEventStore(Protocol):
    def seen_or_record(self, event_id: str) -> bool: ...


@dataclass
class InMemoryWebhookEventStore:
    _events: set[str]

    def __init__(self) -> None:
        self._events = set()
        self._lock = Lock()

    def seen_or_record(self, event_id: str) -> bool:
        with self._lock:
            if event_id in self._events:
                return True
            self._events.add(event_id)
            return False


def derive_event_id(raw_body: bytes, provider_event_id: str | None = None) -> str:
    if provider_event_id:
        return provider_event_id.strip()
    return "sha256:" + sha256(raw_body).hexdigest()
