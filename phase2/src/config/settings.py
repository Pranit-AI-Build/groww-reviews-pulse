"""Configuration settings for Phase 2 Data Processing."""

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
    
    # Storage
    data_dir: Path = Field(default=Path("data"))
    database_path: Path = Field(default=Path("data/reviews.db"))
    
    # Input/Output
    input_db_path: Path = Field(default=Path("../phase1/data/reviews.db"))
    output_db_path: Path = Field(default=Path("data/processed_reviews.db"))
    
    # Logging
    log_level: str = Field(default="INFO")
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.data_dir.mkdir(parents=True, exist_ok=True)


def get_settings() -> Settings:
    """Get application settings singleton."""
    return Settings()
