from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    app_env: str = "development"
    cors_origins: str = "http://localhost:3000"
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()
app = FastAPI(title="Saathi API", version="0.1.0")
app.add_middleware(CORSMiddleware, allow_origins=[x.strip() for x in settings.cors_origins.split(",")], allow_credentials=True, allow_methods=["GET", "POST"], allow_headers=["Content-Type", "Authorization"])

@app.get("/health")
def health():
    return {"status": "ok", "service": "saathi-api", "version": "0.1.0"}

@app.post("/api/v1/conversation")
def conversation(payload: dict):
    message = str(payload.get("message", "")).strip()
    if not message:
        return {"status": "needs_input", "reply": "Namaste! Aap kis baare mein madad chahte hain?"}
    return {"status": "prototype", "reply": "Namaste! Main Saathi hoon. Abhi mera conversation engine taiyar ho raha hai.", "received": True}
