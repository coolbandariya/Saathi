from uuid import uuid4
from fastapi import FastAPI, Header, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware

from .config import get_settings
from .intent import classify_intent
from .schemas import ConversationRequest, ConversationResponse, AgentRequest
from .orchestrator import AgentContext, Orchestrator
from .rate_limit import InMemoryRateLimiter
from .telephony import HmacWebhookVerifier
from .observability import get_correlation_id, set_correlation_id

settings = get_settings()
app = FastAPI(title="Saathi API", version="0.3.0")
app.add_middleware(\n    CORSMiddleware,\n    allow_origins=[x.strip() for x in settings.cors_origins.split(",") if x.strip()],\n    allow_credentials=True,\n    allow_methods=["GET", "POST"],\n    allow_headers=["Content-Type", "Authorization", "X-Saathi-Signature", "X-Correlation-ID"],\n    expose_headers=["X-Correlation-ID"],\n)
limiter = InMemoryRateLimiter()
orchestrator = Orchestrator()\n\n@app.middleware("http")\nasync def correlation_middleware(request: Request, call_next):\n    incoming = request.headers.get("X-Correlation-ID")\n    correlation_id = set_correlation_id(incoming)\n    response = await call_next(request)\n    response.headers["X-Correlation-ID"] = correlation_id\n    return response

@app.get("/health")
def health() -> dict[str, str | bool]:
    return {"status":"ok","service":"saathi-api","version":app.version,"demo_mode":settings.demo_mode}

@app.get("/health/live")
def liveness() -> dict[str,str]:
    return {"status":"alive"}

@app.get("/health/ready")
def readiness() -> dict[str,str | bool]:
    return {"status":"ready","demo_mode":settings.demo_mode}

@app.post("/api/v1/conversation", response_model=ConversationResponse)
def conversation(payload: ConversationRequest, request: Request) -> ConversationResponse:
    key = request.client.host if request.client else "unknown"
    if not limiter.allow(key):
        raise HTTPException(status_code=429, detail="rate_limited")
    intent = classify_intent(payload.message)
    replies = {"scheme":"Bilkul. Main scheme ki jaankari aur required documents samajhne mein madad karunga.","farming":"Bilkul. Main mausam, mandi aur kheti se judi jaankari mein madad karunga.","document":"Document milne par main uska text samajhne aur zaroori action nikalne mein madad kar sakta hoon.","task":"Theek hai. Main is request ko follow-up task ke roop mein rakhne ke liye taiyar hoon.","human":"Theek hai. Main aapki request ko human volunteer ke liye escalate karne ke liye taiyar hoon.","general":"Namaste! Main Saathi hoon. Aap Hindi mein apni zaroorat bata sakte hain."}
    return ConversationResponse(status="ok", reply=replies[intent], intent=intent, demo=settings.demo_mode, correlation_id=get_correlation_id())

@app.post("/api/v1/agent", response_model=ConversationResponse)
async def agent(payload: AgentRequest, request: Request) -> ConversationResponse:
    key = request.client.host if request.client else "unknown"
    if not limiter.allow(f"agent:{key}"):
        raise HTTPException(status_code=429, detail="rate_limited")
    intent, reply, result = await orchestrator.handle(payload.message, AgentContext(household_id=payload.household_id, language=payload.language))
    source = None
    if result and result.source:
        source = {"name":result.source.name,"url":result.source.url,"retrieved_at":result.source.retrieved_at.isoformat(),"freshness_note":result.source.freshness_note}
    return ConversationResponse(status="ok" if result is None or result.ok else "error", reply=reply, intent=intent, source=source, demo=settings.demo_mode, correlation_id=set_correlation_id())

@app.post("/api/v1/webhooks/telephony")
async def telephony_webhook(request: Request, x_saathi_signature: str | None = Header(default=None)) -> dict[str,str | bool]:
    body = await request.body()
    if not settings.telephony_webhook_secret:
        raise HTTPException(status_code=503, detail="telephony_webhook_not_configured")
    if not x_saathi_signature or not HmacWebhookVerifier(settings.telephony_webhook_secret).verify(body, x_saathi_signature):
        raise HTTPException(status_code=401, detail="invalid_signature")
    return {"status":"accepted","event_id":str(uuid4())}
