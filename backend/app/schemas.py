from typing import Literal
from pydantic import BaseModel, Field

Intent = Literal["scheme", "farming", "document", "task", "general", "human"]

class ConversationRequest(BaseModel):
    message: str = Field(min_length=1, max_length=4000)
    household_id: str | None = None
    language: str = Field(default="hi", min_length=2, max_length=16)

class ConversationResponse(BaseModel):
    status: Literal["needs_input", "ok", "error"]
    reply: str
    intent: Intent | None = None
    task_created: bool = False
    request_id: str | None = None
    tool_name: str | None = None
    confidence: float | None = Field(default=None, ge=0, le=1)
