from pathlib import Path

from pydantic import BaseSettings, DirectoryPath, Field


def default_cache_root():
    path = Path() / ".cache"
    if not path.exists():
        path.mkdir()
    return path


class Settings(BaseSettings):
    cache_root: DirectoryPath = Field(default_factory=default_cache_root)

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
