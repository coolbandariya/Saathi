from uuid import uuid4
from fastapi import FastAPI, Header, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from .config import get_settings
from .consent import ConsentState
from .demo import DemoLLM
from .domain import Task
from .intent import classify_intent
from .orchestrator import Orchestrator
from .repositories import InMemoryMemoryStore
from .scheduler import callback_candidates
from .schemas import ConversationRequest, ConversationResponse

settings = get_settings()
app = FastAPI(title="Saathi API", version="0.3.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[x.strip() for x in settings.cors_origins.split(",") if x.strip()],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type", "Authorization", "X-Request-ID"],
)

memory = InMemoryMemoryStore()
orchestrator = Orchestrator(DemoLLM() if settings.demo_mode else None)

@app.get("/health")
def health() -> dict[str, str | bool]:
    return {"status": "ok", "service": "saathi-api", "version": app.version, "demo_mode": settings.demo_mode}

@app.get("/ready")
def ready() -> dict[str, bool]:
    return {"ready": True}

@app.post("/api/v1/conversation", response_model=ConversationResponse)
def conversation(payload: ConversationRequest, x_request_id: str | None = Header(default=None)) -> ConversationResponse:
    request_id = x_request_id or str(uuid4())
    decision = orchestrator.decide(payload.message, payload.language)
    return ConversationResponse(
        status="ok",
        reply=decision.reply,
        intent=decision.intent,
        task_created=False,
        request_id=request_id,
        tool_name=decision.tool_name,
        confidence=decision.confidence,
    )

@app.post("/api/v1/tasks", response_model=Task)
def create_task(task: Task) -> Task:
    if not settings.demo_mode:
        raise HTTPException(status_code=503, detail="Persistent task storage is not configured")
    return memory.create_task(task)

@app.get("/api/v1/tasks/{household_id}", response_model=list[Task])
def get_tasks(household_id: str) -> list[Task]:
    return memory.get_tasks(household_id)

@app.get("/api/v1/callbacks/{household_id}", response_model=list[Task])
def get_callback_candidates(household_id: str) -> list[Task]:
    tasks = memory.get_tasks(household_id)
    consent = ConsentState(household_id=household_id, outbound_calls=False)
    return callback_candidates(tasks, consent)
