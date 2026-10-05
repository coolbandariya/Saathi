from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_env: str = "development"
    cors_origins: str = "http://localhost:3000"
    supabase_url: str | None = None
    supabase_publishable_key: str | None = None
    supabase_secret_key: str | None = None
    llm_provider: str = "gemini"
    llm_model: str = "gemini-2.5-flash"
    gemini_api_key: str | None = None
    openai_api_key: str | None = None
    openai_model: str | None = None
    bhashini_user_id: str | None = None
    bhashini_api_key: str | None = None
    exotel_api_key: str | None = None
    exotel_api_token: str | None = None
    exotel_subdomain: str | None = None
    exotel_virtual_number: str | None = None
    demo_mode: bool = True

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


@lru_cache
def get_settings() -> Settings:
    return Settings()
