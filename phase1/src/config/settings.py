"""Configuration settings for the Groww reviews collector."""

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
    
    # App Configuration
    app_name: str = Field(default="Groww", description="App name")
    playstore_app_id: str = Field(
        default="com.nextbillion.groww",
        description="Play Store app ID"
    )
    playstore_url: str = Field(
        default="https://play.google.com/store/apps/details?id=com.nextbillion.groww&hl=en_IN",
        description="Play Store app URL"
    )
    
    # Review Collection
    weeks_to_collect: int = Field(default=10, ge=1, le=52)
    min_rating: int = Field(default=1, ge=1, le=5)
    max_rating: int = Field(default=5, ge=1, le=5)
    language: str = Field(default="en")
    country: str = Field(default="IN")
    
    # Storage
    data_dir: Path = Field(default=Path("data"))
    database_path: Path = Field(default=Path("data/reviews.db"))
    
    # Logging
    log_level: str = Field(default="INFO")
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Ensure data directory exists
        self.data_dir.mkdir(parents=True, exist_ok=True)


def get_settings() -> Settings:
    """Get application settings singleton."""
    return Settings()
