import time
import contextlib
from aiogram import types
from aiogram.dispatcher.filters import CommandStart

from loader import dp
from keyboards.default import kb_start, kb_worker_menu, kb_admin_start
from data.config import admins

from filters import IsPrivate, IsGroup
from utils.misc import rate_limit
from utils.db_api import worker_commands as worker_commands
from utils.db_api import quick_commands as user_commands


@rate_limit(limit=3)
@dp.message_handler(IsPrivate(), CommandStart())
async def command_start(message: types.Message):
    # args = message.get_args()  # /start 123412
    # new_args = await commands.check_args(args, message.from_user.id)
    # print(new_args)

    try:
        # user = await commands.select_user(message.from_user.id)
        worker = await worker_commands.select_worker(message.from_user.id)
        if worker.user_id in admins:
            await message.answer("🤙Здарова заебал...\n"
                                 "Как дела?\n"
                                 "🐝Шо там все пчелки в улье? Погнали работать?📞", reply_markup=kb_admin_start)

        elif worker.status == 'accepted':
            await message.answer(f'Привет {worker.user_name}\n'
                                 f'Твоя анкета подтверждена, погнали работать.\n', reply_markup=kb_worker_menu)

        elif worker.status == 'created':
            await message.answer('🗂Твоя анкета еще не одобрена.❌\n'
                                 '⏳Ожидай подтверждение администрации.🧑‍💼')

    except Exception:

        await user_commands.add_user(user_id=message.from_user.id,
                                     first_name=message.from_user.first_name,
                                     last_name=message.from_user.last_name,
                                     user_name=message.from_user.username,
                                     status='active')


        # with contextlib.suppress(Exception):
        #     await dp.bot.send_message(chat_id=int(new_args), text=f"По твоей ссылке зарегистрировался {message.from_user.first_name}")

        await message.answer(f"Привет {message.from_user.first_name}!..")
        await message.answer("...🫵Тебя сюда никто не звал, \nно если ты здесь значит тебе что то нужно...")
        time.sleep(2)
        await message.answer("Для начала, пройди регистрацию и если твою анкету одобрят...")
        time.sleep(4)
        await message.answer("Я открою тебе доступ в систему")
        await message.answer("Регистрация по команде /worker_reg")



# @rate_limit(limit=3)
# @dp.message_handler(IsGroup(), text='/ban')
# async def get_ban(message: types.Message):
#     await commands.update_status(user_id=message.from_user.id, status='banned')
#     await message.answer('We are BAN your ass!')


# @rate_limit(limit=3)
# @dp.message_handler(IsGroup(), text='/unban')
# async def get_unban(message: types.Message):
#     await commands.update_status(user_id=message.from_user.id, status='active')
#     await message.answer('You was unbanned from now!')


@rate_limit(limit=3)
@dp.message_handler(IsPrivate(), text='/profile')
async def profile(message: types.Message):
    user = await worker_commands.select_worker(message.from_user.id)
    await message.answer(f'ID = {user.user_id}\n'
                         f'Username = {user.user_name}\n'
                         f'Category = {user.worker_category}\n'
                         f'Status = {user.status}\n'
                         f'Stack = {user.worker_lead_stack}\n'
                         f'Alerts = {user.worker_lead_stack}\n'
                         f'Call Tracker = {user.worker_phone_stats}\n'
                         f'FTDs = {user.worker_deal_stats}')

