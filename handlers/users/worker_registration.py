import logging
import time

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

from data.config import admins
from filters import IsPrivate, IsAdmin
from keyboards.default import kb_worker_menu
from loader import dp
from states.registration import WorkerRegister, Accept
from utils.db_api import worker_commands
from loader import bot


@dp.message_handler(text='Закончить регистрацию',
                    state=[WorkerRegister.u_name,
                           WorkerRegister.w_category,
                           WorkerRegister.w_age,
                           Accept.user_id]
                    )
async def quit_reg(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer('Регистрация отменена', reply_markup=kb_worker_menu)


@dp.message_handler(IsPrivate(), Command('worker_reg'))
async def work_register(message: types.Message):
    name = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text='Закончить регистрацию')
            ]
        ],
        one_time_keyboard=True,
        resize_keyboard=True
    )
    await message.answer(f'Привет {message.from_user.first_name}\n'
                         f'Для начала работы необходимо пройти регистрацию.\n'
                         f'Введи свой рабочий псевдоним (Имя + Фамилия): ',
                         reply_markup=name
                         )
    await WorkerRegister.u_name.set()


@dp.message_handler(IsPrivate(), state=WorkerRegister.u_name)
async def get_worker_name(message: types.Message, state: FSMContext):
    await state.update_data(u_name=message.text)
    categories = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text='Sales Manager'),
                KeyboardButton(text='Retention Manager')
            ],
            [
                KeyboardButton(text='Закончить регистрацию')
            ]
        ],
        one_time_keyboard=True,
        resize_keyboard=True
    )
    await message.answer(f'<b>{message.text}</b>, звучит отлично.')
    time.sleep(1)
    await message.answer('Теперь выбери свой отдел👇', reply_markup=categories)
    await WorkerRegister.w_category.set()


@dp.message_handler(IsPrivate(), state=WorkerRegister.w_category)
async def get_worker_category(message: types.Message, state: FSMContext):
    answer = message.text
    markup = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Закончить регистрацию')]], resize_keyboard=True)

    try:
        if answer == 'Sales Manager' or answer == 'Retention Manager':
            await state.update_data(w_category=answer)
            await message.answer('Отлично. Теперь введи свой возраст целым числом: ', reply_markup=markup)

            await WorkerRegister.w_age.set()
        else:
            await message.answer('Выбери отдел на клавиатуре ниже👇', reply_markup=markup)
    except Exception:
        await message.answer('Выбери отдел на клавиатуре ниже👇', reply_markup=markup)


@dp.message_handler(IsPrivate(), state=WorkerRegister.w_age)
async def get_w_age(message: types.Message, state: FSMContext):
    answer = message.text
    if answer.isnumeric():
        if int(answer) < 80:
            await state.update_data(w_age=answer)
            data = await state.get_data()
            name = data.get('u_name')
            category = data.get('w_category')
            age = data.get('w_age')
            await worker_commands.add_worker_registration(user_id=message.from_user.id,
                                                          first_name=message.from_user.first_name,
                                                          last_name=message.from_user.last_name,
                                                          user_name=name,
                                                          worker_age=age,
                                                          worker_category=category,
                                                          status='created')

            await message.answer(f'✅Регистрация <b>успешно завершена!</b>\n\n'
                                 f'📇Имя: <b>{name}</b>\n'
                                 f'🔞Возраст: <b>{age}</b>\n'
                                 f'🗄Отдел: <b>{category}</b>\n\n'
                                 f'⏳В ближайшее время, ожидайте подтверждения администратором.')
            await state.finish()
        else:
            await message.answer('Введите корректный возраст.(Ты слишком стар для продаж, не пизди мне.)')
    else:
        await message.answer('Введите корректный возраст.(Ты слишком стар для продаж, не пизди мне.)')


@dp.message_handler(IsPrivate(), text="/new_workers", user_id=admins)
async def get_workers(message: types.Message):
    reg = await worker_commands.select_worker_registration()
    # mngr_id = reg.user_id
    ikb = InlineKeyboardMarkup(row_width=1,
                               inline_keyboard=[
                                   [
                                       InlineKeyboardButton(text="Accept",
                                                            callback_data='Accept')
                                   ]
                               ])
    await message.answer(f'Дата создания: <b>{reg.created_at}</b>\n'
                         f'ID: <b>{reg.user_id}</b>\n'
                         f'tg_first_name: <b>{reg.first_name}</b>\n'
                         f'tg_last_name: <b>{reg.last_name}</b>\n'
                         f'Имя: <b>{reg.user_name}</b>\n'
                         f'Категория: <b>{reg.worker_category}</b>\n'
                         f'Статус: <b>{reg.status}</b>',
                         reply_markup=ikb)


@dp.callback_query_handler(text='Accept')
async def accept_w_reg(call: types.CallbackQuery):
    await call.message.answer('Введите айди для подтверждения')
    await Accept.user_id.set()


@dp.message_handler(state=Accept.user_id)
async def accept_reg(message: types.Message, state: FSMContext):
    await worker_commands.accept_w_registration(int(message.text))
    await message.answer(f'Регистрация {message.text} подтверждена')
    await state.finish()

