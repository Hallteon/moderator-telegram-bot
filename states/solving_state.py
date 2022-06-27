from aiogram.dispatcher.filters.state import StatesGroup, State


class Solve_Con_State(StatesGroup):
    start_captcha = State()
    check_captcha = State()