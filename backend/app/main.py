from fastapi import FastAPI, Header, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware

from .config import get_settings
from .intent import classify_intent
from .schemas import ConversationRequest, ConversationResponse, AgentRequest
from .orchestrator import AgentContext, Orchestrator
from .rate_limit import InMemoryRateLimiter
from .telephony import HmacWebhookVerifier
from .observability import get_correlation_id, set_correlation_id
from .webhook_events import InMemoryWebhookEventStore, derive_event_id

settings = get_settings()
app = FastAPI(title="Saathi API", version="0.5.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[x.strip() for x in settings.cors_origins.split(",") if x.strip()],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type", "Authorization", "X-Saathi-Signature", "X-Correlation-ID"],
    expose_headers=["X-Correlation-ID"],
)
limiter = InMemoryRateLimiter()
orchestrator = Orchestrator()
webhook_events = InMemoryWebhookEventStore()

@app.middleware("http")
async def correlation_middleware(request: Request, call_next):
    incoming = request.headers.get("X-Correlation-ID")
    correlation_id = set_correlation_id(incoming)
    response = await call_next(request)
    response.headers["X-Correlation-ID"] = correlation_id
    return response

@app.get("/health")
def health() -> dict[str, str | bool]:
    return {"status":"ok","service":"saathi-api","version":app.version,"demo_mode":settings.demo_mode}

@app.get("/health/live")
def liveness() -> dict[str,str]:
    return {"status":"alive"}

@app.get("/health/ready")
def readiness() -> dict[str,object]:
    telephony = bool(settings.telephony_webhook_secret)
    reasoning = bool(getattr(settings, "gemini_api_key", None) or getattr(settings, "openai_api_key", None))
    status = "ready" if settings.demo_mode or (telephony and reasoning) else "degraded"
    return {"status": status, "demo_mode": settings.demo_mode, "provider_contracts": {"telephony": telephony, "reasoning": reasoning}}

@app.post("/api/v1/conversation", response_model=ConversationResponse)
def conversation(payload: ConversationRequest, request: Request) -> ConversationResponse:
    key = request.client.host if request.client else "unknown"
    if not limiter.allow(key):
        raise HTTPException(status_code=429, detail="rate_limited")
    intent = classify_intent(payload.message)
    replies = {"scheme":"Bilkul. Main scheme ki jaankari aur required documents samajhne mein madad karunga.","farming":"Bilkul. Main mausam, mandi aur kheti se judi jaankari mein madad karunga.","document":"Document milne par main uska text samajhne aur zaroori action nikalne mein madad kar sakta hoon.","task":"Theek hai. Main is request ko follow-up task ke roop mein rakhne ke liye taiyar hoon.","human":"Theek hai. Main aapki request ko human volunteer ke liye escalate karne ke liye taiyar hoon.","general":"Namaste! Main Saathi hoon. Aap Hindi mein apni zaroorat bata sakte hain."}
    escalated = intent == "human"
    return ConversationResponse(status="ok", reply=replies[intent], intent=intent, demo=settings.demo_mode, correlation_id=get_correlation_id(), escalated=escalated, escalation_reason="explicit_human_request" if escalated else None, confidence=1.0 if escalated else 0.85)

@app.post("/api/v1/agent", response_model=ConversationResponse)
async def agent(payload: AgentRequest, request: Request) -> ConversationResponse:
    key = request.client.host if request.client else "unknown"
    if not limiter.allow(f"agent:{key}"):
        raise HTTPException(status_code=429, detail="rate_limited")
    outcome = await orchestrator.handle(payload.message, AgentContext(household_id=payload.household_id, language=payload.language, location=payload.location))
    source = None
    if outcome.result and outcome.result.source:
        source = {"name":outcome.result.source.name,"url":outcome.result.source.url,"retrieved_at":outcome.result.source.retrieved_at.isoformat(),"freshness_note":outcome.result.source.freshness_note}
    failed = bool(outcome.result and not outcome.result.ok)
    return ConversationResponse(status="error" if failed else "ok", reply=outcome.reply, intent=outcome.intent, source=source, demo=settings.demo_mode, correlation_id=get_correlation_id(), escalated=outcome.escalated, escalation_reason=outcome.escalation_reason, confidence=outcome.confidence)

@app.post("/api/v1/webhooks/telephony")
async def telephony_webhook(request: Request, x_saathi_signature: str | None = Header(default=None), x_provider_event_id: str | None = Header(default=None)) -> dict[str,str | bool]:
    body = await request.body()
    if not settings.telephony_webhook_secret:
        raise HTTPException(status_code=503, detail="telephony_webhook_not_configured")
    if not x_saathi_signature or not HmacWebhookVerifier(settings.telephony_webhook_secret).verify(body, x_saathi_signature):
        raise HTTPException(status_code=401, detail="invalid_signature")
    event_id = derive_event_id(body, x_provider_event_id)
    duplicate = webhook_events.seen_or_record(event_id)
    return {"status":"duplicate" if duplicate else "accepted","event_id":event_id}
