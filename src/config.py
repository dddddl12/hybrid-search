from pathlib import Path

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    is_local: bool = False
    database_url: str
    elasticsearch_url: str
    elasticsearch_api_key: str

    class Config:
        env_file = Path(__file__).resolve().parent.parent / ".env"


settings = Settings()
