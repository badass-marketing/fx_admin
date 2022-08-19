from filters import IsPrivate
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from keyboards.default import kb_menu

from loader import dp

# from states import Register


@dp.message_handler(IsPrivate(), Command('register'))
async def register(message: types.Message):
    from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

    name = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=f'{message.from_user.first_name}')
            ]
        ],
        one_time_keyboard=True,
        resize_keyboard=True
    )
    await message.answer("Привет, ты начал регистрацию.\nВведи свое имя", reply_markup=name)
    await Register.name_state.set()


@dp.message_handler(state=Register.name_state)
async def reg_name(message: types.Message, state:FSMContext):
    answer = message.text

    await state.update_data(name_state=answer)
    await message.answer('Cколько тебе полных лет?')
    await Register.age_state.set()


@dp.message_handler(state=Register.age_state)
async def reg_age(message: types.Message, state:FSMContext):
    answer = message.text

    await state.update_data(age_state=answer)
    data = await state.get_data()
    name = data.get('name_state')
    years = data.get('age_state')
    await message.answer('Регистрация успешно завершена\n'
                         f'Твое имя: {name}\n'
                         f'Твой возраст: {years} лет.', reply_markup=kb_menu)
    await state.finish()
