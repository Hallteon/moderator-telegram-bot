from aiogram import types
from aiogram.dispatcher import FSMContext

from loader import dp, bot
from utils.db_utils.db_functions import add_new_user
from utils.inline_keyboards import captcha_menu
from utils.misc.create_captcha import create_conversion
from states.solving_state import Solve_Con_State
from utils.misc.permissions import get_new_user_permissions, get_user_permissions


@dp.message_handler(chat_type=[types.ChatType.GROUP, types.ChatType.SUPERGROUP],
                    content_types=types.ContentTypes.NEW_CHAT_MEMBERS)
async def on_user_join(message: types.Message):
    await message.answer(f"<b>{message.from_user.username}, приветствую тебя в моей группе 👋\n\nЧтобы "
                         f"доказать, что ты не бот, нужно решить пример.</b>", reply_markup=captcha_menu)

    await bot.restrict_chat_member(message.chat.id, message.from_user.id,
                                   permissions=await get_new_user_permissions())

    await Solve_Con_State.first()


@dp.callback_query_handler(chat_type=[types.ChatType.GROUP, types.ChatType.SUPERGROUP],
                           state=Solve_Con_State.start_captcha, text="start_captcha")
async def start_captcha(callback: types.CallbackQuery, state: FSMContext):
    num_one, num_two, nums_sum = await create_conversion()

    await callback.message.edit_text(f"<b>Введите ответ на данный пример: {num_one} + {num_two} = ?</b>")

    async with state.proxy() as data:
        data["num_one"] = num_one
        data["num_two"] = num_two
        data["nums_sum"] = nums_sum
        data["last_msg_id"] = callback.message.message_id

    await Solve_Con_State.next()


@dp.message_handler(chat_type=[types.ChatType.GROUP, types.ChatType.SUPERGROUP],
                    state=Solve_Con_State.check_captcha)
async def check_captcha(message: types.Message, state: FSMContext):
    state_data = await state.get_data()

    if message.text == str(state_data["nums_sum"]):
        await message.answer(f"<b>{message.from_user.username}, мы убедились, что вы не бот. Можете начинать общаться.</b>")
        await bot.restrict_chat_member(message.chat.id, message.from_user.id,
                                       permissions=await get_user_permissions())
        await state.reset_state()

        await add_new_user(message.from_user.id, message.from_user.username)

    else:
        await message.answer(f"<b>{message.from_user.username}, ответ неверный. Пройдите проверку ещё раз.</b>")

        await message.delete()
        await bot.delete_message(message.chat.id, int(state_data["last_msg_id"]))
        await state.reset_state()

        await on_user_join(message)
