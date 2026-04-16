from aiogram import Router
from app.core.config import settings
from app.utils.i18n import I18n
from app.keyboards.language_kb import get_language_keyboard
from app.core.feature_toggle import FeatureToggle
from app.core.ghost_mode import GhostMode

router = Router()

@router.message(lambda msg: msg.text == "/admin")
async def cmd_admin(message):
    if message.from_user.id != settings.OWNER_ID:
        return
    lang = await I18n.get_user_language(message.from_user.id)
    text = I18n.get("menu.admin", lang)
    await message.answer(text)

@router.message(lambda msg: msg.text == "/toggle")
async def cmd_toggle(message):
    if message.from_user.id != settings.OWNER_ID:
        return
    await FeatureToggle.toggle("leech", False)
    await message.answer("✅ Feature toggled")

@router.message(lambda msg: msg.text == "/ghost")
async def cmd_ghost(message):
    if message.from_user.id != settings.OWNER_ID:
        return
    await GhostMode.toggle(message.from_user.id, True)
    await message.answer("👻 Ghost mode activated")
