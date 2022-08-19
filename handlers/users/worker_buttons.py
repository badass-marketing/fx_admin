import time

from aiogram import types

from filters import IsPrivate
from loader import dp, bot

from lead_parser.gmail_parser import *
from keyboards.default import kb_start, kb_worker_data, kb_worker_menu, kb_test, kb_worker_back
from lead_parser.gmail_parser import get_all_unread_json
from data.config import workers, admins
from utils.db_api.worker_commands import update_worker_status
from utils.misc import logging


@dp.message_handler(IsPrivate(), text="Скрипты отдела продаж")
async def worker_skripts(message: types.Message):
    await message.answer(f'Эй {message.from_user.username}! \n'
                         f'Ты выбрал(а) функцию {message.text}.\n'
                         'Вау, похвально! Неужели ты действительно хочешь развиваться?\n'
                         'Тогда держи подгон первый.\n'
                         'Лучше всяких тренингов если будешь учить и применять, а не втыкать.')
    time.sleep(3)
    await message.answer('Ща где то эта ссылка завалялась...')
    time.sleep(10)
    await message.answer('... а вот нашел.')
    time.sleep(2)
    await message.answer('Короче следующие плейлисты <b>обязательны к изучению:</b>\n'
                         '-"Ошибки менеджеров по продажам"\n'
                         '-"РАБОТА С ВОЗРАЖЕНИЯМИ В ПРОДАЖАХ"\n'
                         '-"ХОЛОДНЫЕ ЗВОНКИ МАСТЕР КЛАСС"\n'
                         '-"ПРОДАЖИ ПО ТЕЛЕФОНУ B2C ЗА 50 МИНУТ | БОЙЛЕРНАЯ"\n'
                         '-"ТАК НЕЛЬЗЯ ПРОДАВАТЬ | БОЙЛЕРНАЯ"\n'
                         '-"Универсальные ответы на возражения клиентов"\n'
                         '-"ШКОЛА ПРОДАЖ(что то свежее, сам еще не видел)"\n\n'
                         '<b>ССЫЛКА =></b> https://www.youtube.com/c/Бойлерная408/playlists')
    time.sleep(3)
    await message.answer('😎Надеюсь я не зря стараюсь и это будет кому то полезно. \n😉Не благодари.')


@dp.message_handler(IsPrivate(), text='Статус "Онлайн"')
async def worker_check_in(message: types.Message):
    await update_worker_status(message.from_user.id, status="online")
    await message.answer('Теперь Админ в курсе, что ты на рабочем месте.')
    time.sleep(2)
    await message.answer('Ты сегодня the best!')
    time.sleep(2)
    await message.answer('Скоро админ даст клиентов, жди.', reply_markup=kb_worker_data)
    for admin in admins:
        try:
            text = f"Я {message.from_user.full_name} !\n" \
                   f"Я в сети и полной боевой готовности!\n" \
                   f"Дай работу заебал!"
            await dp.bot.send_message(chat_id=admin, text=text)
        except Exception as err:
            logging.exception(err)
    # TODO: set status to "online"

#
# @dp.message_handler(IsPrivate(), text='Моя статистика', user_id=workers)
# async def worker_stats()
