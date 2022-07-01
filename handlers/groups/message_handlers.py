from aiogram import types

from filters import Is_Bad_Words
from loader import dp
from utils.db_utils.db_functions import add_user_xp


@dp.message_handler(Is_Bad_Words(), chat_type=[types.ChatType.GROUP, types.ChatType.SUPERGROUP])
async def on_message(message: types.Message):
    await add_user_xp(message.from_user.id, 2)