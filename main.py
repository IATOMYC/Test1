import asyncio
import logging
from app.core.bot import bot, dp
from app.core.config import settings
from app.database.engines import close_all, LocalSession, redis_client
from app.database.models import User, Feature, AuditLog
from app.database.base import Base
from app.handlers import admin, user
from app.middlewares.owner_check import OwnerCheckMiddleware
from sqlalchemy import text

logging.basicConfig(level=logging.INFO)

async def init_db():
    async with LocalSession() as session:
        await session.execute(text("PRAGMA foreign_keys=ON"))
        await session.commit()
    async with LocalSession.engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    logging.info("✅ Database initialized")

async def init_redis():
    await redis_client.ping()
    logging.info("✅ Redis connected")

async def init_features():
    async with LocalSession() as session:
        features = ["leech", "vip", "referral", "tasks", "ghost_mode"]
        for key in features:
            result = await session.execute(select(Feature).where(Feature.feature_key == key))
            if not result.scalar_one_or_none():
                session.add(Feature(feature_key=key, is_enabled=True))
        await session.commit()
    logging.info("✅ Features initialized")

async def main():
    await init_db()
    await init_redis()
    await init_features()
    
    dp.include_router(admin.router)
    dp.include_router(user.router)
    
    dp.message.middleware(OwnerCheckMiddleware())
    dp.callback_query.middleware(OwnerCheckMiddleware())
    
    logging.info(" Ultra Master Bot is starting...")
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logging.info("🛑 Bot stopped")
    finally:
        asyncio.run(close_all())
