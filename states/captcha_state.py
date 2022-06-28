from aiogram.dispatcher.filters.state import StatesGroup, State


class Captcha_State(StatesGroup):
    start_captcha = State()
    check_captcha = State()