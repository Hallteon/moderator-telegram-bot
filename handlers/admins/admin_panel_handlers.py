from aiogram import types
from aiogram.dispatcher.filters import Command

from data.config import CHAT_ID
from filters import Is_Admin
from loader import dp, bot
from utils.db_utils.db_functions import get_user_id, get_user_xp, terminate_user
from utils.inline_keyboards import admin_panel, get_all_users_keyboard, get_user_keyboard, back_to_user_menu, \
    back_to_users_keyboard


@dp.message_handler(Command("admin_panel"), Is_Admin(), chat_type=[types.ChatType.PRIVATE])
async def get_admin_panel(message: types.Message):
    await message.answer("<b>Вы вошли в админ-панель.</b>", reply_markup=admin_panel)


@dp.callback_query_handler(text="get_users", chat_type=[types.ChatType.PRIVATE])
async def get_all_users_from_admin_panel(callback: types.CallbackQuery):
    await callback.message.edit_text("Все пользователи группы:")
    await callback.message.edit_reply_markup(reply_markup=await get_all_users_keyboard())


@dp.callback_query_handler(text_contains="get_user", chat_type=[types.ChatType.PRIVATE])
async def get_user_from_admin_panel(callback: types.CallbackQuery):
    user_data = callback.data.split(":")
    user_name = user_data[1].strip()

    await callback.message.edit_text(f"<b>Пользователь {user_name}:</b>")
    await callback.message.edit_reply_markup(reply_markup=await get_user_keyboard(user_name))


@dp.callback_query_handler(text_contains="get_xp", chat_type=[types.ChatType.PRIVATE])
async def get_xp_from_user(callback: types.CallbackQuery):
    user_data = callback.data.split(":")
    user_name = user_data[1].strip()
    user_id = await get_user_id(user_name)
    user_xp = await get_user_xp(user_id)

    await callback.message.edit_text(f"<b>Опыт пользователя {user_name}: {user_xp}xp.</b>")
    await callback.message.edit_reply_markup(reply_markup=await back_to_user_menu(user_name))


@dp.callback_query_handler(text_contains="terminate_user", chat_type=[types.ChatType.PRIVATE])
async def terminate_user_from_group(callback: types.CallbackQuery):
    user_data = callback.data.split(":")
    user_name = user_data[1].strip()
    user_id = await get_user_id(user_name)

    await callback.message.edit_text(f"<b>Пользователь {user_name} был удалён из базы данных и заблокирован "
                                     f"в группе.</b>")
    await callback.message.edit_reply_markup(reply_markup=back_to_users_keyboard)

    await terminate_user(user_id)
    await bot.ban_chat_member(CHAT_ID, user_id)


@dp.callback_query_handler(text_contains="back_to_admin_panel", chat_type=[types.ChatType.PRIVATE])
async def back_to_admin_panel(callback: types.CallbackQuery):
    await callback.message.edit_text("<b>Админ панель.</b>")
    await callback.message.edit_reply_markup(admin_panel)


@dp.callback_query_handler(text_contains="admin_panel_exit", chat_type=[types.ChatType.PRIVATE])
async def exit_from_admin_panel(callback: types.CallbackQuery):
    await callback.message.delete()


@dp.callback_query_handler(text="back_to_all_users", chat_type=[types.ChatType.PRIVATE])
async def back_to_all_users_panel(callback: types.CallbackQuery):
    await get_all_users_from_admin_panel(callback)


@dp.callback_query_handler(text="back_to_user", chat_type=[types.ChatType.PRIVATE])
async def back_to_user_panel(callback: types.CallbackQuery):
    await get_user_from_admin_panel(callback)