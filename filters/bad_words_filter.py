import datetime
from pathlib import Path

from fuzzywuzzy import fuzz
from aiogram import types
from aiogram.dispatcher.filters import BoundFilter

from loader import bot
from utils.db_utils.db_functions import get_mute_time, add_mute_time, remove_user_xp, get_user_xp
from data.permissions import get_muted_user_permissions


class Is_Bad_Words(BoundFilter):

    async def check(self, message: types.Message):
        if message.is_command():
            return False

        else:
            msg_words = message.text.split()
            path = Path("utils", "misc", "bad_words.txt")

            with open(path, "r", encoding="utf-8") as file:
                for word in msg_words:
                    for bad_word in file:
                        equal = fuzz.ratio(word.lower(), bad_word.lower())

                        if equal >= 75:
                            await message.delete()

                            mute_time = await get_mute_time(message.from_user.id)
                            await message.answer(f"<b>Пользователю {message.from_user.username} был выдан мут "
                                                 f"на {mute_time} минут. В следующий раз это время увеличится "
                                                 f"в два раза!</b>")

                            mute_time = datetime.timedelta(minutes=mute_time)

                            await bot.restrict_chat_member(message.chat.id, message.from_user.id,
                                                           permissions=await get_muted_user_permissions(),
                                                           until_date=datetime.datetime.now() + mute_time)

                            await add_mute_time(message.from_user.id)

                            xp = await get_user_xp(message.from_user.id)

                            if xp < 5:
                                await remove_user_xp(message.from_user.id, xp)

                            else:
                                await remove_user_xp(message.from_user.id, 5)

                            return False

            return True
