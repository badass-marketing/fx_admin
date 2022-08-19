from aiogram import types
from loader import dp
from keyboards.default import kb_test


@dp.message_handler(text='Main Menu')
async def command_start(message: types.Message):
    await message.answer(f'Hello {message.from_user.full_name}!\n'
                         f'Here must be some text', reply_markup=kb_test)
