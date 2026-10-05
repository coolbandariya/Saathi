from datetime import datetime, timezone
from pydantic import BaseModel, Field

class SourceRecord(BaseModel):
    name: str = Field(min_length=1, max_length=120)
    url: str = Field(min_length=1, max_length=1000)
    retrieved_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    freshness_note: str | None = Field(default=None, max_length=300)

class ToolResult(BaseModel):
    ok: bool
    data: dict = Field(default_factory=dict)
    source: SourceRecord | None = None
    error_code: str | None = None
    retryable: bool = False
