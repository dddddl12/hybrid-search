from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from app.core.config import settings

assert (settings.database_name
        and settings.database_username
        and settings.database_password
        and settings.database_host)
DATABASE_URL = f"postgresql+asyncpg://{settings.database_username}:{settings.database_password}@{settings.database_host}:{settings.database_port}/{settings.database_name}"
Base = declarative_base()
engine = create_async_engine(DATABASE_URL)
