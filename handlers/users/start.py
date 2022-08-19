from aiogram import types
from loader import dp
from keyboards.default import kb_start

from filters import IsPrivate

from utils.misc import rate_limit


@rate_limit(limit=3)
@dp.message_handler(IsPrivate(), text='/start')
async def command_start(message: types.Message):
    await message.answer(f'Hello {message.from_user.full_name}!\n'
                         f'Your id: {message.from_user.id}')
