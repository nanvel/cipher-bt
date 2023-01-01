from pathlib import Path

from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    cache_root: Path = Field(default=".cache")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
