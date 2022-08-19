from aiogram import types
from loader import dp


@dp.message_handler(text=['Привет', 'Hello', 'hello', 'привет'])
async def command_hello(message: types.Message):
    await message.answer(f'Hello great and smart {message.from_user.first_name}!\n'
                         'How u doing?')
