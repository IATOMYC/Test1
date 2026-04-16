import json
from typing import Dict, Any
from app.database.engines import redis_client

class DynamicEngine:
    @staticmethod
    async def get_ui_config(lang: str = "en") -> Dict[str, Any]:
        cached = await redis_client.get(f"ui_config:{lang}")
        if cached:
            return json.loads(cached)
        return await DynamicEngine._load_default_config(lang)

    @staticmethod
    async def _load_default_config(lang: str) -> Dict[str, Any]:
        default = {
            "features": {"leech": True, "vip": True, "ghost": False},
            "buttons": {"show_welcome": True, "show_help": True}
        }
        await redis_client.setex(f"ui_config:{lang}", 300, json.dumps(default))
        return default

    @staticmethod
    async def reload_ui():
        cursor = 0
        while True:
            cursor, keys = await redis_client.scan(cursor, match="ui_config:*", count=100)
            if keys:
                await redis_client.delete(*keys)
            if cursor == 0:
                break
