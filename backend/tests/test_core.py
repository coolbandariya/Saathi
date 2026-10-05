from datetime import datetime, timedelta, timezone
from app.consent import ConsentState, can_make_outbound_call
from app.documents import DocumentExtraction, review_gate, validate_upload
from app.orchestrator import Orchestrator
from app.repositories import InMemoryMemoryStore
from app.scheduler import callback_candidates, due_tasks
from app.telephony import WebhookReplayGuard, parse_exotel_event, verify_hmac_signature
from app.domain import Task

def test_orchestrator_routes_demo_llm():
    decision = Orchestrator().decide("mujhe scholarship scheme ki jaankari chahiye")
    assert decision.intent == "scheme"

def test_memory_store_isolates_households():
    store = InMemoryMemoryStore()
    store.create_task(Task(id="a", household_id="h1", title="A"))
    store.create_task(Task(id="b", household_id="h2", title="B"))
    assert [x.id for x in store.get_tasks("h1")] == ["a"]
    assert store.complete_task("h1", "b") is None

def test_callback_requires_explicit_consent_and_quiet_hours():
    now = datetime(2026, 10, 6, 12, tzinfo=timezone.utc)
    task = Task(id="a", household_id="h1", title="callback", due_at=now - timedelta(minutes=1), outbound_consent=True)
    consent = ConsentState(household_id="h1", outbound_calls=True, quiet_hours_start=21, quiet_hours_end=8)
    assert callback_candidates([task], consent, now) == [task]

def test_callback_blocked_during_quiet_hours():
    now = datetime(2026, 10, 6, 22, tzinfo=timezone.utc)
    task = Task(id="a", household_id="h1", title="callback", due_at=now - timedelta(minutes=1), outbound_consent=True)
    consent = ConsentState(household_id="h1", outbound_calls=True)
    assert callback_candidates([task], consent, now) == []

def test_document_review_gate():
    low = review_gate(DocumentExtraction(text="x", confidence=.5))
    high = review_gate(DocumentExtraction(text="x", confidence=.95))
    assert low.needs_human_review is True
    assert high.needs_human_review is False

def test_document_upload_validation():
    validate_upload("application/pdf", 100, "notice.pdf")
    for args in [("application/msword", 100, "a.doc"), ("application/pdf", 0, "a.pdf"), ("application/pdf", 100, "../a.pdf")]:
        try:
            validate_upload(*args)
            assert False
        except ValueError:
            pass

def test_webhook_replay_guard():
    guard = WebhookReplayGuard()
    assert guard.accept("evt-1") is True
    assert guard.accept("evt-1") is False

def test_webhook_signature():
    body=b'{"event":"start"}'
    import hashlib, hmac
    signature=hmac.new(b"secret", body, hashlib.sha256).hexdigest()
    assert verify_hmac_signature(body, signature, "secret") is True
    assert verify_hmac_signature(body, "bad", "secret") is False

def test_exotel_event_parser():
    event = parse_exotel_event('{"event":"media","stream_sid":"s1","media":{"payload":"abc"}}')
    assert event.event == "media"
    assert event.stream_sid == "s1"
    assert event.payload == "abc"
