from datetime import datetime, timezone
from enum import StrEnum
from pydantic import BaseModel, Field

class CallDirection(StrEnum):
    INBOUND = "inbound"
    OUTBOUND = "outbound"

class CallStatus(StrEnum):
    RECEIVED = "received"
    CONNECTING = "connecting"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    ESCALATED = "escalated"

class CallRecord(BaseModel):
    call_id: str
    household_id: str | None = None
    phone_number: str = Field(min_length=7, max_length=20)
    direction: CallDirection
    status: CallStatus = CallStatus.RECEIVED
    provider: str
    provider_call_id: str | None = None
    language: str = "hi"
    started_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    ended_at: datetime | None = None
