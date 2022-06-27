from aiogram import types
from aiogram.dispatcher.filters import CommandHelp

from loader import dp


@dp.message_handler(CommandHelp(), chat_type=[types.ChatType.GROUP, types.ChatType.SUPERGROUP])
async def command_help(message: types.Message):
    await message.answer("<b>Доступные команды в группе:\n/xp - посмотреть своё количество опыта.\n"
                         "/</b>")


