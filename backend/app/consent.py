from dataclasses import dataclass
from datetime import datetime, timezone

from .domain import ConsentType


@dataclass(frozen=True)
class ConsentDecision:
    allowed: bool
    reason: str


def evaluate_consent(
    *,
    consent_type: ConsentType,
    granted: bool,
    recorded_at: datetime | None,
    now: datetime | None = None,
) -> ConsentDecision:
    if not granted:
        return ConsentDecision(False, f"{consent_type.value}_consent_required")
    if recorded_at is None:
        return ConsentDecision(False, f"{consent_type.value}_consent_timestamp_required")

    current = now or datetime.now(timezone.utc)
    timestamp = recorded_at if recorded_at.tzinfo else recorded_at.replace(tzinfo=timezone.utc)
    if timestamp > current:
        return ConsentDecision(False, "consent_timestamp_in_future")

    return ConsentDecision(True, "consent_granted")
