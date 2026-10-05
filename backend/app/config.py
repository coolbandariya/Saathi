from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_env: str = "development"
    cors_origins: str = "http://localhost:3000"
    supabase_url: str | None = None
    supabase_publishable_key: str | None = None
    supabase_secret_key: str | None = None
    llm_provider: str = "gemini"
    llm_model: str = "gemini-3.8-flash"
    gemini_api_key: str | None = None
    openai_api_key: str | None = None
    openai_model: str | None = None
    speech_provider: str = "sarvam"
    bhashini_user_id: str | None = None
    bhashini_api_key: str | None = None
    bhashini_stt_endpoint: str | None = None
    bhashini_tts_endpoint: str | None = None
    sarvam_api_key: str | None = None
    sarvam_stt_endpoint: str = "https://api.sarvam.ai/speech-to-text"
    sarvam_stt_model: str = "saaras:v4"
    sarvam_tts_endpoint: str = "https://api.sarvam.ai/text-to-speech"
    sarvam_tts_model: str = "bulbul:v3"
    sarvam_tts_speaker: str = "shubh"
    mandi_api_key: str | None = None
    mandi_resource_id: str | None = None
    mandi_api_base: str = "https://api.data.gov.in/resource"
    exotel_api_key: str | None = None
    exotel_api_token: str | None = None
    exotel_account_sid: str | None = None
    exotel_subdomain: str = "api.in.exotel.com"
    exotel_virtual_number: str | None = None
    telephony_webhook_secret: str | None = None
    demo_mode: bool = True
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


@lru_cache
def get_settings() -> Settings:
    return Settings()
