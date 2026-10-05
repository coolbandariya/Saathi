from collections import defaultdict, deque
from time import monotonic


class InMemoryRateLimiter:
    """Small local/demo limiter. Production should use a shared store."""
    def __init__(self, limit: int = 30, window_seconds: int = 60, max_keys: int = 10_000) -> None:
        self.limit = limit
        self.window_seconds = window_seconds
        self.max_keys = max_keys
        self._events: dict[str, deque[float]] = defaultdict(deque)

    def allow(self, key: str) -> bool:
        now = monotonic()
        events = self._events[key]
        while events and now - events[0] > self.window_seconds:
            events.popleft()

        if not events and len(self._events) > self.max_keys:
            oldest_key = min(
                self._events,
                key=lambda candidate: self._events[candidate][-1] if self._events[candidate] else now,
            )
            self._events.pop(oldest_key, None)
            events = self._events[key]

        if len(events) >= self.limit:
            return False
        events.append(now)
        return True
