import json
import os
from typing import Dict, Any
from functools import lru_cache

class I18n:
    _translations: Dict[str, Dict[str, Any]] = {}
    
    @classmethod
    def load_language(cls, lang: str) -> Dict[str, Any]:
        if lang not in cls._translations:
            locales_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "locales")
            file_path = os.path.join(locales_dir, f"{lang}.json")
            if os.path.exists(file_path):
                with open(file_path, "r", encoding="utf-8") as f:
                    cls._translations[lang] = json.load(f)
            else:
                with open(os.path.join(locales_dir, "en.json"), "r", encoding="utf-8") as f:
                    cls._translations[lang] = json.load(f)
        return cls._translations[lang]
    
    @classmethod
    def get(cls, key: str, lang: str = "en", **kwargs) -> str:
        data = cls.load_language(lang)
        keys = key.split(".")
        value = data
        for k in keys:
            value = value.get(k, {}) if isinstance(value, dict) else {}
        if not value:
            return key
        if isinstance(value, str) and kwargs:
            for k, v in kwargs.items():
                value = value.replace(f"{{{k}}}", str(v))
        return value
    
    @classmethod
    def set_language(cls, user_id: int, lang: str):
        from app.database.engines import redis_client
        import asyncio
        asyncio.run(redis_client.setex(f"user_lang:{user_id}", 86400, lang))
    
    @classmethod
    async def get_user_language(cls, user_id: int) -> str:
        from app.database.engines import redis_client
        lang = await redis_client.get(f"user_lang:{user_id}")
        return lang.decode() if lang else "en"
