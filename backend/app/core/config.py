"""Backend configuration settings."""

from pathlib import Path
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings."""
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )
    
    # App
    app_name: str = Field(default="Groww Reviews API")
    debug: bool = Field(default=False)
    
    # Server
    host: str = Field(default="0.0.0.0")
    port: int = Field(default=8000)
    
    # Data paths
    data_dir: Path = Field(default=Path("../phase2/data"))
    reports_dir: Path = Field(default=Path("../phase3/outputs"))
    
    # Email settings (for Phase 6)
    smtp_host: str = Field(default="")
    smtp_port: int = Field(default=587)
    smtp_user: str = Field(default="")
    smtp_password: str = Field(default="")
    email_from: str = Field(default="")
    
    @property
    def database_path(self) -> Path:
        return self.data_dir / "processed_reviews.db"
    
    @property
    def latest_report_path(self) -> Path:
        return self.reports_dir / "weekly_pulse.json"


def get_settings() -> Settings:
    return Settings()
