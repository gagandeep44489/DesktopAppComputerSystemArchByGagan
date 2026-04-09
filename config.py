"""Application configuration classes."""

from __future__ import annotations

import os
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
DEFAULT_SQLITE_FILE = (BASE_DIR / "instance" / "insurance_claims.db").resolve()


class Config:
    """Base configuration."""

    SECRET_KEY = os.getenv("SECRET_KEY", "change-this-in-production")
    _database_url = os.getenv("DATABASE_URL", "").strip()
    SQLALCHEMY_DATABASE_URI = _database_url or f"sqlite:///{DEFAULT_SQLITE_FILE.as_posix()}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAX_CONTENT_LENGTH = 5 * 1024 * 1024  # 5 MB
    UPLOAD_FOLDER = BASE_DIR / "app" / "uploads"
    ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "pdf"}


class DevelopmentConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    DEBUG = False


config_by_name = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
}
