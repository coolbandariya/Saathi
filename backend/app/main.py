from base64 import b64encode

from fastapi import FastAPI, File, Form, Header, HTTPException, Request, UploadFile
from fastapi.middleware.cors import CORSMiddleware

from .config import get_settings
from .intent import classify_intent
from .schemas import AgentRequest, ConversationRequest, ConversationResponse, VoiceTurnResponse
from .orchestrator import AgentContext, Orchestrator
from .rate_limit import InMemoryRateLimiter
from .telephony import HmacWebhookVerifier
from .observability import get_correlation_id, set_correlation_id
from .voice import VoiceGateway
from .webhook_events import InMemoryWebhookEventStore, derive_event_id


settings = get_settings()
app = FastAPI(title="Saathi API", version="0.6.0")
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
voice_gateway = VoiceGateway(settings, orchestrator)


@app.middleware("http")
async def correlation_middleware(request: Request, call_next):
    incoming = request.headers.get("X-Correlation-ID")
    correlation_id = set_correlation_id(incoming)
    response = await call_next(request)
    response.headers["X-Correlation-ID"] = correlation_id
    return response


@app.get("/health")
def health() -> dict[str, str | bool]:
    return {"status": "ok", "service": "saathi-api", "version": app.version, "demo_mode": settings.demo_mode}


@app.get("/health/live")
def liveness() -> dict[str, str]:
    return {"status": "alive"}


@app.get("/health/ready")
def readiness() -> dict[str, object]:
    telephony = bool(settings.telephony_webhook_secret and settings.exotel_api_key and settings.exotel_api_token and settings.exotel_account_sid and settings.exotel_virtual_number and settings.exotel_stream_url)
    reasoning = bool(getattr(settings, "gemini_api_key", None) or getattr(settings, "openai_api_key", None))
    mandi = bool(settings.mandi_api_key and settings.mandi_resource_id)
    speech = bool(
        (settings.bhashini_api_key and settings.bhashini_stt_endpoint and settings.bhashini_tts_endpoint)
        or settings.sarvam_api_key
    )
    status = "ready" if settings.demo_mode or (telephony and reasoning and mandi and speech) else "degraded"
    return {
        "status": status,
        "demo_mode": settings.demo_mode,
        "provider_contracts": {
            "telephony": telephony,
            "reasoning": reasoning,
            "mandi": mandi,
            "speech": speech,
            "weather": True,
        },
    }


@app.post("/api/v1/conversation", response_model=ConversationResponse)
async def conversation(payload: ConversationRequest, request: Request) -> ConversationResponse:
    key = request.client.host if request.client else "unknown"
    if not limiter.allow(key):
        raise HTTPException(status_code=429, detail="rate_limited")
    outcome = await orchestrator.handle(
        payload.message,
        AgentContext(
            household_id=payload.household_id,
            language=payload.language,
            location=payload.location,
        ),
    )
    source = None
    if outcome.result and outcome.result.source:
        source = {
            "name": outcome.result.source.name,
            "url": outcome.result.source.url,
            "retrieved_at": outcome.result.source.retrieved_at.isoformat(),
            "freshness_note": outcome.result.source.freshness_note,
        }
    failed = bool(outcome.result and not outcome.result.ok)
    return ConversationResponse(
        status="error" if failed else "ok",
        reply=outcome.reply,
        intent=outcome.intent,
        source=source,
        demo=settings.demo_mode,
        correlation_id=get_correlation_id(),
        escalated=outcome.escalated,
        escalation_reason=outcome.escalation_reason,
        confidence=outcome.confidence,
    )

@app.post("/api/v1/agent", response_model=ConversationResponse)
async def agent(payload: AgentRequest, request: Request) -> ConversationResponse:
    key = request.client.host if request.client else "unknown"
    if not limiter.allow(f"agent:{key}"):
        raise HTTPException(status_code=429, detail="rate_limited")
    outcome = await orchestrator.handle(
        payload.message,
        AgentContext(household_id=payload.household_id, language=payload.language, location=payload.location),
    )
    source = None
    if outcome.result and outcome.result.source:
        source = {
            "name": outcome.result.source.name,
            "url": outcome.result.source.url,
            "retrieved_at": outcome.result.source.retrieved_at.isoformat(),
            "freshness_note": outcome.result.source.freshness_note,
        }
    failed = bool(outcome.result and not outcome.result.ok)
    return ConversationResponse(
        status="error" if failed else "ok",
        reply=outcome.reply,
        intent=outcome.intent,
        source=source,
        demo=settings.demo_mode,
        correlation_id=get_correlation_id(),
        escalated=outcome.escalated,
        escalation_reason=outcome.escalation_reason,
        confidence=outcome.confidence,
    )


@app.post("/api/v1/voice/turn", response_model=VoiceTurnResponse)
async def voice_turn(
    request: Request,
    audio: UploadFile = File(...),
    language: str = Form("hi"),
    household_id: str | None = Form(None),
) -> VoiceTurnResponse:
    key = request.client.host if request.client else "unknown"
    if not limiter.allow(f"voice:{key}"):
        raise HTTPException(status_code=429, detail="rate_limited")
    allowed_audio_types = {"audio/webm", "audio/wav", "audio/x-wav", "audio/ogg", "audio/mp4", "audio/mpeg"}
    if audio.content_type and audio.content_type not in allowed_audio_types:
        raise HTTPException(status_code=415, detail="unsupported_audio_type")
    if len(language) < 2 or len(language) > 20:
        raise HTTPException(status_code=422, detail="invalid_language")
    if household_id is not None and (len(household_id) < 1 or len(household_id) > 120):
        raise HTTPException(status_code=422, detail="invalid_household_id")
    max_audio_bytes = 8_000_000
    raw = await audio.read(max_audio_bytes + 1)
    if not raw:
        raise HTTPException(status_code=422, detail="empty_audio")
    if len(raw) > max_audio_bytes:
        raise HTTPException(status_code=413, detail="audio_too_large")
    try:
        turn = await voice_gateway.handle(raw, language=language, household_id=household_id)
    except RuntimeError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=502, detail="voice_provider_error") from exc

    source = None
    if turn.outcome.result and turn.outcome.result.source:
        source = {
            "name": turn.outcome.result.source.name,
            "url": turn.outcome.result.source.url,
            "retrieved_at": turn.outcome.result.source.retrieved_at.isoformat(),
            "freshness_note": turn.outcome.result.source.freshness_note,
        }
    return VoiceTurnResponse(
        status="ok",
        transcript=turn.transcript,
        reply=turn.outcome.reply,
        intent=turn.outcome.intent,
        audio_base64=b64encode(turn.audio).decode("ascii") if turn.audio else None,
        audio_mime_type="audio/wav" if turn.audio else None,
        source=source,
        demo=settings.demo_mode,
        correlation_id=get_correlation_id(),
        escalated=turn.outcome.escalated,
        escalation_reason=turn.outcome.escalation_reason,
        confidence=turn.outcome.confidence,
    )


@app.post("/api/v1/webhooks/telephony")
async def telephony_webhook(
    request: Request,
    x_saathi_signature: str | None = Header(default=None),
    x_provider_event_id: str | None = Header(default=None),
) -> dict[str, str | bool]:
    body = await request.body()
    if not settings.telephony_webhook_secret:
        raise HTTPException(status_code=503, detail="telephony_webhook_not_configured")
    if not x_saathi_signature or not HmacWebhookVerifier(settings.telephony_webhook_secret).verify(body, x_saathi_signature):
        raise HTTPException(status_code=401, detail="invalid_signature")
    event_id = derive_event_id(body, x_provider_event_id)
    duplicate = webhook_events.seen_or_record(event_id)
    return {"status": "duplicate" if duplicate else "accepted", "event_id": event_id}
