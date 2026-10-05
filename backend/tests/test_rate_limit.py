from app.rate_limit import InMemoryRateLimiter


def test_rate_limiter_evicts_oldest_key_at_capacity(monkeypatch):
    limiter = InMemoryRateLimiter(limit=2, window_seconds=60, max_keys=2)
    clock = iter([1.0, 2.0, 3.0])
    monkeypatch.setattr("app.rate_limit.monotonic", lambda: next(clock))

    assert limiter.allow("first")
    assert limiter.allow("second")
    assert limiter.allow("third")

    assert len(limiter._events) == 2
    assert "first" not in limiter._events
    assert "second" in limiter._events
    assert "third" in limiter._events


def test_rate_limiter_rejects_invalid_configuration():
    try:
        InMemoryRateLimiter(limit=0)
    except ValueError:
        pass
    else:
        raise AssertionError("invalid limiter configuration was accepted")
