from app.database.engines import redis_client

class GhostMode:
    @staticmethod
    async def is_active(user_id: int) -> bool:
        return bool(await redis_client.get(f"ghost:{user_id}"))

    @staticmethod
    async def toggle(user_id: int, state: bool):
        if state:
            await redis_client.setex(f"ghost:{user_id}", 86400, "1")
        else:
            await redis_client.delete(f"ghost:{user_id}")
