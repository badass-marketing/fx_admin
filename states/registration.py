from aiogram.dispatcher.filters.state import StatesGroup, State


class Accept(StatesGroup):
    user_id = State()


class LeadAddState(StatesGroup):
    lead_name = State()
    phone = State()
    email = State()
    sources = State()
    age = State()


class WorkerRegister(StatesGroup):
    u_name = State()
    w_category = State()
    w_age = State()

