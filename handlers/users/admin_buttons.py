import time

from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from filters import IsPrivate
from keyboards.default.kb_admin import kb_admin_hub
from loader import dp

from lead_parser.gmail_parser import *
from keyboards.default import kb_start, kb_worker_data, kb_worker_menu, kb_test, kb_worker_back, kb_admin_data, kb_admin_start
from lead_parser.gmail_parser import get_all_unread_json
from data.config import admins
from keyboards.default import kb_admin_squad


# @dp.message_handler(text='Get Leads')
# async def buttons_test(message: types.Message):
#     await message.answer(f'Hey {message.from_user.username}! \n'
#                          f'{message.text} is a  working function.\n'
#                          'Its not working for now.\n'
#                          'Have patience.')
from states import Accept
from utils.db_api.worker_commands import select_accepted_workers, select_created_workers, select_online_workers, \
    get_workers_online


@dp.message_handler(IsPrivate(), text='Получить данные', user_id=admins)
async def buttons_test(message: types.Message):
    await message.answer(f'Эй {message.from_user.username}! \n'
                         f'Ты выбрал функцию {message.text}.\n'
                         'Бережно обращайся с данными.\n'
                         'Они денег стоят.', reply_markup=kb_admin_data)


@dp.message_handler(IsPrivate(), text='Выгрузить все непрочитанные', user_id=admins)
async def buttons_test(message: types.Message):
    result = []
    await message.answer('Проверяю наличие непрочитанных писем...')

    get_all_unread_json()

    with open("/Users/pax/PycharmProjects/fx24_tg_admin/lead_parser/storage/result.json") as file:
        forms_data = json.load(file)
        print(forms_data)

    for form_data in forms_data:
        date = form_data['date']
        time = form_data['time']
        name = form_data['lead_name']
        email = form_data['email']
        phone = form_data['phone']
        source = form_data['source']
        pole_data = form_data['pole_data']

        array = [date, time, name, email, phone, source, pole_data]
        result.append(array)

        with open("/Users/pax/PycharmProjects/fx24_tg_admin/lead_parser/storage/result.csv", "w") as file:
            writer = csv.writer(file)  # delimeter can be present

            writer.writerow(
                (
                    'Date',
                    'Time',
                    'Name',
                    'Email',
                    'Phone Number',
                    'Client Source',
                    'Pole Data'
                )
            )

            writer.writerows(
                result
            )

    await message.reply_document(open('/Users/pax/PycharmProjects/fx24_tg_admin/lead_parser/storage/result.csv', 'rb'))
    await message.answer("Ваш догумент готов.\n"
                         "Отметить все новые письма как прочитанные?"
                         )


# @dp.message_handler(text='Книга')
# async def buttons_test(message: types.Message):
#     await message.answer('Собираю данные в файл...')
#     await get_books_from_gmail_api()
#
#
#     await message.reply_document(open('lead_parser/storage/result.csv', 'rb'))
#     await message.answer("Ваш догумент готов.\n"
#                          "Пометить сообщения прочитанными?\n"
#                          "Отметятся ВСЕ непрочитанные!")
#
#
# @dp.message_handler(text='Илон')
# async def buttons_test(message: types.Message):
#     await message.answer('Собираю данные в файл...')
#     await get_ilon()
#
#     await message.reply_document(open('lead_parser/storage/result.csv', 'rb'))
#     await message.answer("Ваш догумент готов.\n"
#                          "Пометить сообщения прочитанными?\n"
#                          "Отметятся ВСЕ непрочитанные!")
#
#
# @dp.message_handler(text='Маргулан')
# async def buttons_test(message: types.Message):
#     await message.answer('Собираю данные в файл...')
#     await get_margulan()
#
#     await message.reply_document(open('lead_parser/storage/result.csv', 'rb'))
#     await message.answer("Ваш догумент готов.\n"
#                          "Пометить сообщения прочитанными?\n"
#                          "Отметятся ВСЕ непрочитанные!")


@dp.message_handler(text='Отметить прочитанными')
async def buttons_test(message: types.Message):
    await message.answer('Читаю сообщения...')

    await mark_as_read()
    await message.answer('Все сообщения прочитаны!', reply_markup=kb_admin_start)
    await message.delete()


@dp.message_handler(text='Назад')
async def buttons_test(message: types.Message):
    await message.answer(f'Воу {message.from_user.username}! \n'
                         f'Мы еще не закончили?', reply_markup=kb_admin_start)


@dp.message_handler(text='[*]SMS Bomber')
async def buttons_test(message: types.Message):
    await message.answer(f'Hey {message.from_user.username}! \n'
                         f'{message.text} is a Function\nto make a joke on a friend or punish a bad person😈.\n'
                         'Its not working for now.\n'
                         'Have patience.')


@dp.message_handler(text="Мой SuiSquad")
async def my_squad(message: types.Message):
    await message.answer("Заглянем в улей.", reply_markup=kb_admin_squad)


@dp.message_handler(text='Просмотреть пчел "онлайн"')
async def my_desk_online(message: types.Message):
    worker = await get_workers_online()
    for bee in worker:
        await message.answer(f"status: {bee.status}\n"
                             f"Name: {bee.user_name}")
        # else:
        #     await message.answer("Нет никого онлайн.\n"
        #                          "Сегодня уикенд что ли?🧐")


@dp.message_handler(text="Просмотреть очередь в улей", user_id=admins)
async def all_created_workers(message: types.Message):
    worker = await select_created_workers()
    ikb = InlineKeyboardMarkup(row_width=1,
                               inline_keyboard=[
                                   [
                                       InlineKeyboardButton(text="Accept",
                                                            callback_data='accept'),
                                       InlineKeyboardButton(text="Decline",
                                                            callback_data='decline')
                                   ]
                               ])
    for bee in worker:
        await message.answer(f"User-Name: {bee.user_name}\n"
                             f"Name: {bee.first_name}"
                             f"Status: {bee.status}\n"
                             f"ID: {bee.user_id}",
                             reply_markup=ikb)


@dp.callback_query_handler(text='accept')
async def accept_w_reg(call: types.CallbackQuery):
    await call.message.answer('Введите айди для подтверждения')
    await Accept.user_id.set()


@dp.callback_query_handler(text='decline')
async def decline_w_reg(call: types.CallbackQuery):
    await call.message.answer()



@dp.message_handler(text="Мой Лид Хаб")
async def lead_hub(message: types.Message):
    await message.answer("Поглядим есть что у нас здесь...", reply_markup=kb_admin_hub)


# @dp.message_handler(text="Подтвердить новые заявки")
# async def apply_new_leadforms(message: types.Message):
