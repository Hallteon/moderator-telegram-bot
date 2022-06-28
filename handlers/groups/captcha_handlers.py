import asyncio

from aiogram import types
from aiogram.dispatcher import FSMContext

from loader import dp, bot
from states.captcha_state import Captcha_State
from utils.db_utils.db_functions import add_new_user
from utils.misc.create_captcha import create_captcha
from utils.misc.permissions import get_new_user_permissions, get_user_permissions, get_muted_user_permissions


@dp.message_handler(chat_type=[types.ChatType.GROUP, types.ChatType.SUPERGROUP],
                    content_types=types.ContentTypes.NEW_CHAT_MEMBERS)
async def on_user_join(message: types.Message):
    await message.reply(f"<b>{message.from_user.username}, приветствую вас в моей группе 👋</b>")

    await bot.restrict_chat_member(message.chat.id, message.from_user.id,
                                   permissions=await get_new_user_permissions())

    await Captcha_State.first()


@dp.message_handler(chat_type=[types.ChatType.GROUP, types.ChatType.SUPERGROUP],
                    state=Captcha_State.start_captcha)
async def start_solving_captcha(message: types.Message, state: FSMContext):
    mode, one_num, two_num, sum_num = await create_captcha()

    await message.delete()
    ans = await message.answer(f"<b>{message.from_user.username}, перед тем как вы начнёте "
                         f"Общаться в группе, решите пример:\n\n{one_num} {mode} {two_num} = ?</b>")

    async with state.proxy() as data:
        data["mode"] = mode
        data["one_num"] = one_num
        data["two_num"] = two_num
        data["sum_num"] = sum_num
        data["answer"] = ans

    await Captcha_State.next()


@dp.message_handler(chat_type=[types.ChatType.GROUP, types.ChatType.SUPERGROUP],
                    state=Captcha_State.check_captcha)
async def check_captcha(message: types.Message, state: FSMContext):
    state_data = await state.get_data()

    await state_data["answer"].delete()

    if str(state_data["sum_num"]) == message.text.strip():
        await message.delete()
        await message.answer(f"<b>{message.from_user.username}, вы прошли капчу и мы убедились, что вы не бот. Можете "
                             "начинать общаться.</b>")

        await state.reset_state()

        await add_new_user(message.from_user.id, message.from_user.username)
        await bot.restrict_chat_member(message.chat.id, message.from_user.id,
                                       permissions=await get_user_permissions())

    else:
        await state.reset_state()
        ans = await message.answer(f"<b>{message.from_user.username}, вы не прошли капчу. "
                             f"Повторите попытку через минуту.</b>")

        await bot.restrict_chat_member(message.chat.id, message.from_user.id,
                                       permissions=await get_muted_user_permissions())

        await state.reset_state()
        await asyncio.sleep(5)
        await ans.delete()

        await bot.restrict_chat_member(message.chat.id, message.from_user.id,
                                       permissions=await get_new_user_permissions())

        await Captcha_State.first()
        await start_solving_captcha(message, state)

