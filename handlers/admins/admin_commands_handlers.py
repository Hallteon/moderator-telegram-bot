import datetime

from aiogram import types
from aiogram.dispatcher.filters import AdminFilter, Command

from loader import dp, bot
from utils.db_utils.db_functions import get_user_id
from data.permissions import get_muted_user_permissions, get_user_permissions


@dp.message_handler(Command("mute"), AdminFilter())
async def mute_member(message: types.Message):
    try:
        message_args = message.get_args().split()

        await message.delete()

        if len(message_args) == 1:
            muted_user_id = int(await get_user_id(message_args[0][1:]))

            await message.answer(f"<b>{message.from_user.username} выдал мут пользователю {message_args[0][1:]} на "
                                 f"неопределённый срок.</b>")

            await bot.restrict_chat_member(message.chat.id, muted_user_id,
                                           permissions=await get_muted_user_permissions())

        elif len(message_args) == 3:
            muted_user_id = int(await get_user_id(message_args[0][1:]))
            mute_time_mode = message_args[1]
            num_time = 0

            if mute_time_mode == "minutes":
                num_time = datetime.timedelta(minutes=float(message_args[2]))

            elif mute_time_mode == "hours":
                num_time = datetime.timedelta(hours=float(message_args[2]))

            elif mute_time_mode == "days":
                num_time = datetime.timedelta(days=float(message_args[2]))

            await message.answer(f"<b>{message.from_user.username} выдал мут пользователю {message_args[0][1:]} на "
                                 f"{num_time}.</b>")

            await bot.restrict_chat_member(message.chat.id, muted_user_id,
                                           permissions=await get_muted_user_permissions(),
                                           until_date=datetime.datetime.now() + num_time)

        else:
            await message.answer("<b>Пожалуйста, передайте недостающие аргументы или уберите лишние. "
                                 "Вы можете посмотреть инструкции к админ-командам в админ-панеле бота.</b>")

    except:
        await message.answer("<b>Видимо вы допустили ошибку при передаче аргументов. "
                             "Вы можете посмотреть инструкции к админ-командам в админ-панеле бота.</b>")


@dp.message_handler(Command("unmute"), AdminFilter())
async def unmute_member(message: types.Message):
    try:
        message_args = message.get_args().split()

        await message.delete()

        if len(message_args) == 1:
            muted_user_id = int(await get_user_id(message_args[0][1:]))

            await message.answer(f"<b>{message.from_user.username} снял мут с пользователя "
                                 f"{message_args[0][1:]}.</b>")

            await bot.restrict_chat_member(message.chat.id, muted_user_id,
                                           permissions=await get_user_permissions())

        else:
            await message.answer("<b>Пожалуйста, передайте недостающие аргументы или уберите лишние. "
                                 "Вы можете посмотреть инструкции к админ-командам в админ-панеле бота.</b>")

    except:
        await message.answer("<b>Видимо вы допустили ошибку при передаче аргументов. "
                             "Вы можете посмотреть инструкции к админ-командам в админ-панеле бота.</b>")


@dp.message_handler(Command("ban"), AdminFilter())
async def ban_member(message: types.Message):
    try:
        message_args = message.get_args().split()

        await message.delete()

        if len(message_args) == 1:
            muted_user_id = int(await get_user_id(message_args[0][1:]))

            await message.answer(f"<b>{message.from_user.username} выдал бан пользователю {message_args[0][1:]} на "
                                 f"неопределённый срок.</b>")

            await bot.ban_chat_member(message.chat.id, muted_user_id)

        elif len(message_args) == 3:
            muted_user_id = int(await get_user_id(message_args[0][1:]))
            mute_time_mode = message_args[1]
            num_time = 0

            if mute_time_mode == "minutes":
                num_time = datetime.timedelta(minutes=float(message_args[2]))

            elif mute_time_mode == "hours":
                num_time = datetime.timedelta(hours=float(message_args[2]))

            elif mute_time_mode == "days":
                num_time = datetime.timedelta(days=float(message_args[2]))

            await message.answer(f"<b>{message.from_user.username} выдал бан пользователю {message_args[0][1:]} на "
                                 f"{num_time}.</b>")

            await bot.ban_chat_member(message.chat.id, muted_user_id,
                                      until_date=datetime.datetime.now() + num_time)

        else:
            await message.answer("<b>Пожалуйста, передайте недостающие аргументы или уберите лишние. "
                                 "Вы можете посмотреть инструкции к админ-командам в админ-панеле бота.</b>")

    except:
        await message.answer("<b>Видимо вы допустили ошибку при передаче аргументов. "
                             "Вы можете посмотреть инструкции к админ-командам в админ-панеле бота.</b>")


@dp.message_handler(Command("unban"), AdminFilter())
async def unban_member(message: types.Message):
    try:
        message_args = message.get_args().split()

        await message.delete()

        if len(message_args) == 1:
            muted_user_id = int(await get_user_id(message_args[0][1:]))

            await message.answer(f"<b>{message.from_user.username} снял бан с пользователя "
                                 f"{message_args[0][1:]}.</b>")

            await bot.unban_chat_member(message.chat.id, muted_user_id,
                                        only_if_banned=True)

        else:
            await message.answer("<b>Пожалуйста, передайте недостающие аргументы или уберите лишние. "
                                 "Вы можете посмотреть инструкции к админ-командам в админ-панеле бота.</b>")

    except:
        await message.answer("<b>Видимо вы допустили ошибку при передаче аргументов. "
                             "Вы можете посмотреть инструкции к админ-командам в админ-панеле бота.</b>")


        
