from pathlib import Path
from typing import Optional

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    is_local: bool = False
    elasticsearch_url: str
    elasticsearch_api_key: str

    database_name: Optional[str] = None
    database_username: Optional[str] = None
    database_password: Optional[str] = None
    database_host: Optional[str] = None
    database_port: int = 5432

    class Config:
        env_file = Path(__file__).resolve().parent.parent.parent / ".env"


settings = Settings()
