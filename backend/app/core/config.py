from pathlib import Path
from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent.parent

class Settings(BaseSettings):
    PROJECT_NAME: str = "OmniPost AI"
    API_V1_STR: str = "/api"
    DATABASE_URL: str = f"sqlite:///{BASE_DIR}/social_marketing.db"
    STORAGE_DIR: Path = BASE_DIR / "storage"
    
    # AI API Keys
    GEMINI_API_KEY: Optional[str] = None
    GROQ_API_KEY: Optional[str] = None
    PEXELS_API_KEY: Optional[str] = None
    
    # Social Media API Credentials (optional for live publishing)
    META_ACCESS_TOKEN: Optional[str] = None
    LINKEDIN_ACCESS_TOKEN: Optional[str] = None
    TIKTOK_ACCESS_TOKEN: Optional[str] = None
    YOUTUBE_API_KEY: Optional[str] = None
    
    # Platform Behavior
    DEMO_MODE: bool = True
    ALLOW_ORIGINS: list[str] = ["http://localhost:5173", "http://127.0.0.1:5173", "http://localhost:3000"]

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()

# Ensure storage directories exist
(settings.STORAGE_DIR / "uploads").mkdir(parents=True, exist_ok=True)
(settings.STORAGE_DIR / "generated").mkdir(parents=True, exist_ok=True)
