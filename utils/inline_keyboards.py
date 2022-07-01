from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

from utils.db_utils.db_functions import get_all_users

user_callback = CallbackData("get_user", "user_name")
user_xp_callback = CallbackData("get_xp", "user_name")
user_delete_callback = CallbackData("terminate_user", "user_name")

admin_panel = InlineKeyboardMarkup()

admin_panel.add(InlineKeyboardButton(text="Пользователи", callback_data="get_users"))
admin_panel.add(InlineKeyboardButton(text="Выйти из админ-панели", callback_data="admin_panel_exit"))

back_to_users_keyboard = InlineKeyboardMarkup()

back_to_users_keyboard.add(InlineKeyboardButton(text="Назад", callback_data="back_to_all_users"))


async def get_all_users_keyboard():
    all_users_keyboard = InlineKeyboardMarkup()
    all_users = await get_all_users()

    for user in all_users.keys():
        all_users_keyboard.insert(InlineKeyboardButton(text=f"{user}",
                                                       callback_data=user_callback.new(user)))

    all_users_keyboard.add(InlineKeyboardButton(text="Назад", callback_data="back_to_admin_panel"))

    return all_users_keyboard


async def get_user_keyboard(name):
    user_keyboard = InlineKeyboardMarkup()

    user_keyboard.add(InlineKeyboardButton(text="Опыт", callback_data=user_xp_callback.new(name)))
    user_keyboard.add(InlineKeyboardButton(text="Удалить из БД и заблокировать", callback_data=user_delete_callback.new(name)))
    user_keyboard.add(InlineKeyboardButton(text="Назад", callback_data="back_to_all_users"))

    return user_keyboard


async def back_to_user_menu(name):
    back_to_user_keyboard = InlineKeyboardMarkup()
    back_to_user_keyboard.insert(InlineKeyboardButton(text="Назад", callback_data=user_callback.new(name)))

    return back_to_user_keyboard

