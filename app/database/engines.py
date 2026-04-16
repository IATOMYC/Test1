from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from motor.motor_asyncio import AsyncIOMotorClient
import redis.asyncio as aioredis
from app.core.config import settings

local_engine = create_async_engine(settings.LOCAL_DB_PATH, echo=False)
LocalSession = sessionmaker(local_engine, class_=AsyncSession, expire_on_commit=False)

cloud_engines = {}
for name, url in [("supabase", settings.SUPABASE_URL), ("neon", settings.NEON_URL), ("cockroach", settings.COCKROACH_URL)]:
    if url:
        cloud_engines[name] = create_async_engine(url, echo=False, pool_pre_ping=True)

mongo_client = AsyncIOMotorClient(settings.MONGO_URL) if settings.MONGO_URL else None
mongo_db = mongo_client.ultra_master if mongo_client else None

redis_pool = aioredis.ConnectionPool.from_url(settings.REDIS_URL)
redis_client = aioredis.Redis(connection_pool=redis_pool)

async def close_all():
    await redis_client.aclose()
    for eng in cloud_engines.values(): await eng.dispose()
    await local_engine.dispose()
    if mongo_client: mongo_client.close()
