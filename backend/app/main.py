from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .config import get_settings
from .intent import classify_intent
from .schemas import ConversationRequest, ConversationResponse

settings = get_settings()
app = FastAPI(title="Saathi API", version="0.2.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[x.strip() for x in settings.cors_origins.split(",") if x.strip()],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type", "Authorization"],
)


@app.get("/health")
def health() -> dict[str, str | bool]:
    return {"status": "ok", "service": "saathi-api", "version": app.version, "demo_mode": settings.demo_mode}


@app.post("/api/v1/conversation", response_model=ConversationResponse)
def conversation(payload: ConversationRequest) -> ConversationResponse:
    intent = classify_intent(payload.message)
    replies = {
        "scheme": "Bilkul. Main scheme ki jaankari aur required documents samajhne mein madad karunga.",
        "farming": "Bilkul. Main mausam, mandi aur kheti se judi jaankari mein madad karunga.",
        "document": "Document milne par main uska text samajhne aur zaroori action nikalne mein madad kar sakta hoon.",
        "task": "Theek hai. Main is request ko follow-up task ke roop mein rakhne ke liye taiyar hoon.",
        "human": "Theek hai. Main aapki request ko human volunteer ke liye escalate karne ke liye taiyar hoon.",
        "general": "Namaste! Main Saathi hoon. Aap Hindi mein apni zaroorat bata sakte hain.",
    }
    return ConversationResponse(status="ok", reply=replies[intent], intent=intent)
