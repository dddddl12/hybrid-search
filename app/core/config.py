from pathlib import Path
from typing import Optional

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=Path(__file__).resolve().parent.parent.parent / ".env",
        env_file_encoding='utf-8'
    )

    is_local: bool = False
    elasticsearch_url: str
    elasticsearch_api_key: str

    database_name: Optional[str] = None
    database_username: Optional[str] = None
    database_password: Optional[str] = None
    database_host: Optional[str] = None
    database_port: int = 5432


settings = Settings()
