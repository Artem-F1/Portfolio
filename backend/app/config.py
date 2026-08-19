from pydantic_settings import BaseSettings
from typing import List, Union
import os


class Settings(BaseSettings):
    app_name: str = "Todo list"
    debug: bool = True
    database_url: str = os.getenv("DATABASE_URL", "postgresql+asyncpg://postgres:postgres@localhost:5432/task_db")
    redis_url: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    cache_ttl_seconds: int = 1800
    cache_tasks_key: str ="cache:tasks_list"
    cors_origins: Union[List[str], str] = [
        "http://localhost:5173",
        "http://localhost:3000",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:3000",
    ]

    class Config:
        env_file = ".env"

settings = Settings()
