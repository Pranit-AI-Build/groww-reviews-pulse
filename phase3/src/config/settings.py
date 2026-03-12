"""Configuration settings for Phase 3 Analysis."""

from pathlib import Path
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )
    
    # Groq API
    groq_api_key: str = Field(..., description="Groq API Key")
    groq_model: str = Field(default="llama-3.3-70b-versatile", description="Groq Model")
    
    # Input/Output
    input_db_path: Path = Field(default=Path("../phase2/data/processed_reviews.db"))
    output_dir: Path = Field(default=Path("outputs"))
    
    # Analysis Settings
    max_themes: int = Field(default=5, ge=1, le=10)
    max_quotes: int = Field(default=3, ge=1, le=10)
    max_actions: int = Field(default=3, ge=1, le=10)
    
    # Logging
    log_level: str = Field(default="INFO")
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.output_dir.mkdir(parents=True, exist_ok=True)


def get_settings() -> Settings:
    """Get application settings singleton."""
    return Settings()
