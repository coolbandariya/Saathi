from typing import Literal
from pydantic import BaseModel, Field

Intent = Literal["scheme", "farming", "document", "task", "general", "human"]
EscalationReason = Literal["low_confidence", "explicit_human_request", "provider_failure", "safety_boundary"]

class ConversationRequest(BaseModel):
    message: str = Field(min_length=1, max_length=4000)
    household_id: str | None = Field(default=None, min_length=1, max_length=120)
    language: str = Field(default="hi", min_length=2, max_length=20)

class SourceResponse(BaseModel):
    name: str
    url: str
    retrieved_at: str
    freshness_note: str | None = None

class ConversationResponse(BaseModel):
    status: Literal["needs_input", "ok", "error"]
    reply: str
    intent: Intent | None = None
    task_created: bool = False
    source: SourceResponse | None = None
    demo: bool = False
    correlation_id: str | None = None
    escalated: bool = False
    escalation_reason: EscalationReason | None = None
    confidence: float | None = Field(default=None, ge=0.0, le=1.0)

class AgentRequest(ConversationRequest):
    pass
