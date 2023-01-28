from pathlib import Path

from pydantic import BaseSettings, Field

from cipher.models import LogLevel


class Settings(BaseSettings):
    cache_root: Path = Field(default=".cache")
    log_level: LogLevel = Field(default=LogLevel.INFO)

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
