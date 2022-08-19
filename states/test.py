from aiogram.dispatcher.filters.state import StatesGroup, State


class Register(StatesGroup):
    name_state = State()
    age_state = State()
