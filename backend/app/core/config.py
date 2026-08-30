from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Central place for environment-driven configuration.
    Reads from .env in local dev, real env vars in deployment.
    """

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    APP_NAME: str = "FlowPay Engine API"
    ENVIRONMENT: str = "development"

    # Database
    DATABASE_URL: str = "postgresql+psycopg2://postgres:postgres@localhost:5432/flowpay"

    # CORS - comma separated origins in env, parsed into a list
    ALLOWED_ORIGINS: str = "http://localhost:3000"

    # Engine tuning constants (kept here so hackathon judges see tunables in one place)
    SHOCK_RATIO_THRESHOLD: float = 0.55
    LEAN_RATIO_THRESHOLD: float = 0.80
    STRONG_RATIO_THRESHOLD: float = 1.25
    FORECAST_MIN_SPREAD: float = 0.10
    FORECAST_MAX_SPREAD: float = 0.35

    @property
    def allowed_origins_list(self) -> list[str]:
        return [origin.strip() for origin in self.ALLOWED_ORIGINS.split(",") if origin.strip()]


@lru_cache
def get_settings() -> Settings:
    # Cached so we don't re-parse env vars on every request
    return Settings()
