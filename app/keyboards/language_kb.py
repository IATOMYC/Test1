from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

def get_language_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    languages = [
        ("العربية 🇸🇦", "ar"),
        ("English 🇺", "en"),
        ("Español 🇪🇸", "es"),
        ("Français 🇫🇷", "fr"),
        ("Deutsch 🇩🇪", "de"),
        ("Русский 🇷🇺", "ru"),
        ("中文 🇨🇳", "zh"),
        ("हिन्दी 🇮🇳", "hi"),
        ("Português 🇵🇹", "pt"),
        ("Türkçe 🇹", "tr"),
        ("Tiếng Việt 🇻🇳", "vi"),
        ("Bahasa Indonesia 🇮🇩", "id"),
    ]
    for text, code in languages:
        builder.button(text=text, callback_data=f"lang_{code}")
    builder.adjust(2)
    return builder.as_markup()

def get_back_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="↩️ Back", callback_data="back")
    return builder.as_markup()
