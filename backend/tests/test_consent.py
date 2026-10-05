from datetime import datetime, timezone

from app.consent import evaluate_consent
from app.domain import ConsentType


def test_consent_requires_explicit_grant():
    result = evaluate_consent(
        consent_type=ConsentType.MEMORY,
        granted=False,
        recorded_at=datetime.now(timezone.utc),
    )
    assert not result.allowed
    assert result.reason == "memory_consent_required"


def test_consent_rejects_future_timestamp():
    result = evaluate_consent(
        consent_type=ConsentType.OUTBOUND_CALLS,
        granted=True,
        recorded_at=datetime(2030, 1, 1, tzinfo=timezone.utc),
        now=datetime(2029, 1, 1, tzinfo=timezone.utc),
    )
    assert not result.allowed
    assert result.reason == "consent_timestamp_in_future"


def test_consent_allows_recorded_grant():
    timestamp = datetime(2026, 10, 1, tzinfo=timezone.utc)
    result = evaluate_consent(
        consent_type=ConsentType.DOCUMENT_PROCESSING,
        granted=True,
        recorded_at=timestamp,
        now=datetime(2026, 10, 5, tzinfo=timezone.utc),
    )
    assert result.allowed
