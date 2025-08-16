from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

from cipher.models import LogLevel


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    cache_root: Path = ".cache"
    log_level: LogLevel = LogLevel.INFO
