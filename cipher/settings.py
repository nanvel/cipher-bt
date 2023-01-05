from pydantic import BaseSettings, DirectoryPath, Field


class Settings(BaseSettings):
    cache_root: DirectoryPath = Field(default=".cache")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
