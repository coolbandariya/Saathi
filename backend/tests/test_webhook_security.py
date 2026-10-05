import hashlib
import hmac

from app.webhook_security import IdempotencyLedger, verify_hmac_signature


def test_webhook_signature_uses_constant_time_comparison():
    payload = b'{"event":"call.completed"}'
    secret = "test-secret"
    digest = hmac.new(secret.encode(), payload, hashlib.sha256).hexdigest()

    assert verify_hmac_signature(
        payload=payload,
        signature=f"sha256={digest}",
        secret=secret,
    )


def test_webhook_rejects_wrong_signature():
    assert not verify_hmac_signature(
        payload=b"payload",
        signature="sha256=" + "0" * 64,
        secret="test-secret",
    )


def test_idempotency_ledger_rejects_duplicates():
    ledger = IdempotencyLedger()
    assert ledger.accept("evt_123")
    assert not ledger.accept("evt_123")
    assert not ledger.accept(" ")
