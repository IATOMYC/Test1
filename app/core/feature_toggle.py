import json
from app.database.engines import redis_client

class FeatureToggle:
    @staticmethod
    async def is_enabled(feature_key: str) -> bool:
        val = await redis_client.get(f"feature:{feature_key}")
        if val is None:
            return True
        return val.decode() == "1"

    @staticmethod
    async def toggle(feature_key: str, state: bool):
        val = "1" if state else "0"
        await redis_client.setex(f"feature:{feature_key}", 3600, val)
        await redis_client.publish("feature_updates", json.dumps({"key": feature_key, "state": state}))
