from functools import lru_cache
from typing import List

from pydantic import HttpUrl
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    PROJECT_NAME: str = "EsthetiManage API"
    API_V1_PREFIX: str = "/api/v1"
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24
    DATABASE_URL: str
    REDIS_URL: str | None = None
    TWILIO_ACCOUNT_SID: str | None = None
    TWILIO_AUTH_TOKEN: str | None = None
    TWILIO_FROM_NUMBER: str | None = None
    STRIPE_SECRET_KEY: str | None = None
    STRIPE_WEBHOOK_SECRET: str | None = None
    GOOGLE_SERVICE_ACCOUNT_FILE: str | None = None
    ALLOWED_ORIGINS: List[HttpUrl] = []
    SENTRY_DSN: str | None = None


@lru_cache
def get_settings() -> Settings:
    return Settings()
