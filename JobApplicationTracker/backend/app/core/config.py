from __future__ import annotations

from pathlib import Path
from typing import Set

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "Job Application Tracker"
    database_url: str = "sqlite:///./app.db"

    # File upload settings
    upload_dir: Path = Path("uploads")
    max_file_size: int = 10 * 1024 * 1024  # 10MB
    allowed_extensions: Set[str] = {".pdf", ".doc", ".docx"}

    class Config:
        env_file = ".env"


settings = Settings()

# Ensure upload directories exist
settings.upload_dir.mkdir(exist_ok=True)
(settings.upload_dir / "resumes").mkdir(exist_ok=True)
(settings.upload_dir / "cover_letters").mkdir(exist_ok=True)
