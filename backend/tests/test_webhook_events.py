from app.webhook_events import InMemoryWebhookEventStore, derive_event_id


def test_event_id_is_deterministic_without_provider_id():
    assert derive_event_id(b"same-body") == derive_event_id(b"same-body")
    assert derive_event_id(b"same-body") != derive_event_id(b"other-body")


def test_provider_event_id_takes_precedence():
    assert derive_event_id(b"body", "evt-123") == "evt-123"


def test_store_detects_duplicates():
    store = InMemoryWebhookEventStore()
    assert store.seen_or_record("evt-123") is False
    assert store.seen_or_record("evt-123") is True


def test_store_deduplicates_concurrent_replays():
    from concurrent.futures import ThreadPoolExecutor

    store = InMemoryWebhookEventStore()
    with ThreadPoolExecutor(max_workers=16) as pool:
        outcomes = list(pool.map(store.seen_or_record, ["same-event"] * 64))

    assert outcomes.count(False) == 1
    assert outcomes.count(True) == 63
