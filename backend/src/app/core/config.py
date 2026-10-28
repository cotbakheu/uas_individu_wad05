from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "UMKM Operational API"
    environment: str = "development"
    secret_key: str = "change-me-in-development"
    csrf_secret_key: str = "change-me-csrf-in-development"
    database_url: str = "sqlite:///./umkm_local.db"
    frontend_url: str = "http://localhost:5173"
    session_cookie_name: str = "umkm_session"
    session_cookie_secure: bool = False
    session_cookie_samesite: str = "lax"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


@lru_cache
def get_settings() -> Settings:
    return Settings()
