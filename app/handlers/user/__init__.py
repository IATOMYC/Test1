from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from app.utils.i18n import I18n
from app.keyboards.language_kb import get_language_keyboard
from app.database.engines import redis_client
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.models.user import User
from app.database.engines import LocalSession

router = Router()

@router.message(F.command == "start")
async def cmd_start(message: Message):
    lang = message.from_user.language_code or "en"
    if len(lang) > 2:
        lang = lang.split("-")[0]
    
    async with LocalSession() as session:
        result = await session.execute(select(User).where(User.telegram_id == message.from_user.id))
        user = result.scalar_one_or_none()
        if not user:
            user = User(
                telegram_id=message.from_user.id,
                username=message.from_user.username,
                full_name=message.from_user.full_name or "User",
                language_code=lang
            )
            session.add(user)
            await session.commit()
        else:
            user.language_code = lang
            await session.commit()
    
    await redis_client.setex(f"user_lang:{message.from_user.id}", 86400, lang)
    
    text = I18n.get("welcome.title", lang) + "\n\n" + I18n.get("welcome.select_lang", lang)
    await message.answer(text, reply_markup=get_language_keyboard())

@router.callback_query(F.data.startswith("lang_"))
async def cb_language(callback: CallbackQuery):
    lang = callback.data.split("_")[1]
    user_id = callback.from_user.id
    
    await redis_client.setex(f"user_lang:{user_id}", 86400, lang)
    
    async with LocalSession() as session:
        result = await session.execute(select(User).where(User.telegram_id == user_id))
        user = result.scalar_one_or_none()
        if user:
            user.language_code = lang
            await session.commit()
    
    text = I18n.get("welcome.language_selected", lang)
    await callback.answer(text, show_alert=True)
    await callback.message.delete()
    
    text = I18n.get("welcome.title", lang) + "\n\n" + I18n.get("menu.main", lang)
    await callback.message.answer(text)
