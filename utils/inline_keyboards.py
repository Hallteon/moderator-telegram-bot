from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

captcha_menu = InlineKeyboardMarkup()

captcha_menu.insert(InlineKeyboardButton(text="Решить пример 🧩", callback_data="start_captcha"))
