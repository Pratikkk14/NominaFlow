"""Configuration settings for NominaFlow application."""

import os
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application runtime configuration."""

    APP_NAME: str = "NominaFlow"
    APP_VERSION: str = "0.1.0"
    DEBUG: bool = False

    # Database Configuration (Defaults to SQLite for frictionless local/CI runs, overrides via env for PostgreSQL)
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./nominaflow.db")

    # Security & Authentication
    SECRET_KEY: str = os.getenv("SECRET_KEY", "nominaflow-insecure-development-secret-key-2026")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440  # 24 hours

    # Uploads Storage
    UPLOAD_DIR: Path = Path(os.getenv("UPLOAD_DIR", "uploads"))
    MAX_FILE_SIZE_BYTES: int = 5 * 1024 * 1024  # 5 MB
    ALLOWED_MIME_TYPES: list[str] = [
        "application/pdf",
        "image/png",
        "image/jpeg",
        "image/jpg",
    ]

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")


settings = Settings()

# Ensure uploads directory exists
settings.UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
