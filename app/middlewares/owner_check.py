from typing import Callable, Dict, Any, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery
from app.core.config import settings

class OwnerCheckMiddleware(BaseMiddleware):
    async def __call__(self, handler: Callable[[Message | CallbackQuery, Dict[str, Any]], Awaitable[Any]], event: Message | CallbackQuery, data: Dict[str, Any]) -> Any:
        user_id = None
        if isinstance(event, Message):
            user_id = event.from_user.id
        elif isinstance(event, CallbackQuery):
            user_id = event.from_user.id
        if user_id != settings.OWNER_ID:
            return None
        return await handler(event, data)
