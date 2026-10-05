from collections import deque
from time import monotonic


class InMemoryRateLimiter:
    """Small local/demo limiter. Production should use a shared store."""

    def __init__(self, limit: int = 30, window_seconds: int = 60, max_keys: int = 10_000) -> None:
        if limit < 1 or window_seconds < 1 or max_keys < 1:
            raise ValueError("rate_limiter_configuration_must_be_positive")
        self.limit = limit
        self.window_seconds = window_seconds
        self.max_keys = max_keys
        self._events: dict[str, deque[float]] = {}

    def allow(self, key: str) -> bool:
        now = monotonic()
        events = self._events.get(key)

        if events is None:
            if len(self._events) >= self.max_keys:
                oldest_key = min(
                    self._events,
                    key=lambda candidate: self._events[candidate][-1] if self._events[candidate] else now,
                )
                self._events.pop(oldest_key, None)
            events = deque()
            self._events[key] = events

        while events and now - events[0] > self.window_seconds:
            events.popleft()

        if len(events) >= self.limit:
            return False
        events.append(now)
        return True
