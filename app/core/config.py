from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    BOT_TOKEN: str
    OWNER_ID: int
    LOCAL_DB_PATH: str = "sqlite+aiosqlite:///ultra_local.db"
    SUPABASE_URL: Optional[str] = None
    NEON_URL: Optional[str] = None
    MONGO_URL: Optional[str] = None
    COCKROACH_URL: Optional[str] = None
    REDIS_URL: str = "redis://localhost:6379/0"

    class Config:
        env_file = ".env"
        case_sensitive = False

settings = Settings()
