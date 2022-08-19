import time
import json
import os

import datetime
from aiogram import types
from collections import Counter
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

from data.config import admins
from filters import IsPrivate, IsAdmin
from keyboards.inline.inline_kb_admin_menu import ikb_menu_apply
from loader import dp
from utils.db_api import register_lead_commands
from lead_parser.gmail_parser import get_all_unread_json


@dp.message_handler(IsPrivate(), Command('leadregister'), user_id=admins)
async def lead_register(message: types.Message):
    cur_time = time.time()
    # name = ReplyKeyboardMarkup(
    #     keyboard=[
    #         [
    #             KeyboardButton(text='Непрочитанные в JSON')
    #         ]
    #     ],
    #     resize_keyboard=True,
    #     one_time_keyboard=True
    # )
    # await message.answer('Давай попробуем загрузить лид-форму в базу данных.',
    #                      reply_markup=name)
    await message.answer('Собираю заявки...')
    get_all_unread_json()

# @dp.message_handler(IsPrivate(), text='Непрочитанные в JSON')
# async def load_json(message: types.Message):

    await message.answer('Формирую файл JSON...')


    await message.answer('JSON файл сформирован\n'
                         'Все непрочитанные собраны...')

    await message.answer('Открываю файл с заявками.')

    with open('lead_parser/storage/result.json', 'r') as json_file:
        data_j = json.load(json_file)
        for data in data_j:
            lead_name = data['lead_name']
            email = data['email']
            phone = data['phone']
            source = data['source']
            pole_data = data['pole_data']

            await register_lead_commands.new_lead_registration(lead_name=lead_name,
                                                               phone=phone,
                                                               email=email,
                                                               source=source,
                                                               pole_data=pole_data,
                                                               status='created')
            time.sleep(1)

            await message.answer(f'Name: {lead_name}\n'
                                 f'phone: {phone}\n'
                                 f'email: {email}\n'
                                 f'source: {source}\n'
                                 f'pole_data: {pole_data}\n'
                                 f'status: "created"')

        await message.answer('Поздравляю, Сэр.\n'
                             'Все новыe заявки внесены в базу данных.\n'
                             'Желаете продолжить работу с БД?')


@dp.message_handler(IsPrivate(), text='/lead_registrations', user_id=admins)
async def get_reg(message: types.Message):
    reg = await register_lead_commands.select_lead_registration()

    await message.answer(f'Дата создания: {reg.created_at}\n'
                         f'ID: {reg.lead_id}\n'
                         f'Имя: {reg.lead_name}\n'
                         f'Телефон: {reg.phone}\n'
                         f'Иcточник: {reg.source}\n'
                         f'Результат опроса: {reg.pole_data}', reply_markup=ikb_menu_apply)


@dp.message_handler(IsPrivate(), text='/lead_glypi', user_id=admins)
async def get_reg(message: types.Message):
    reg = await register_lead_commands.select_all_glypi()
    for regs in reg:
        await message.answer(f'Дата создания: {regs.created_at}\n'
                             f'ID: {regs.lead_id}\n'
                             f'Имя: {regs.lead_name}\n'
                             f'Телефон: {regs.phone}\n'
                             f'Иcточник: {regs.source}\n'
                             f'Результат опроса: {regs.pole_data}', reply_markup=ikb_menu_apply)


@dp.message_handler(IsPrivate(), text='/lead_ilon', user_id=admins)
async def get_reg(message: types.Message):
    reg = await register_lead_commands.select_all_ilon()
    # for regs in reg:
    await message.answer(f'Дата создания: {reg.created_at}\n'
                         f'ID: {reg.lead_id}\n'
                         f'Имя: {reg.lead_name}\n'
                         f'Телефон: {reg.phone}\n'
                         f'Иcточник: {reg.source}\n'
                         f'Результат опроса: {reg.pole_data}', reply_markup=ikb_menu_apply)


@dp.message_handler(IsPrivate(), text='/lead_marg', user_id=admins)
async def get_reg(message: types.Message):
    reg = await register_lead_commands.select_all_margulan()
    # for regs in reg:
    await message.answer(f'Дата создания: {reg.created_at}\n'
                         f'Status: {reg.status}\n'
                         f'ID: {reg.lead_id}\n'
                         f'Имя: {reg.lead_name}\n'
                         f'Телефон: {reg.phone}\n'
                         f'Иcточник: {reg.source}\n'
                         f'Результат опроса: {reg.pole_data}', reply_markup=ikb_menu_apply)





