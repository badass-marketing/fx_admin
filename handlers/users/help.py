from aiogram import types
from loader import dp


@dp.message_handler(text=['/help', 'help'])
async def command_help(message: types.Message):
    await message.answer(f'Great and smart {message.from_user.full_name} needs help? \n'
                         'Lets wait untill the creator would give me the Power!\n\n'
                         'In the meantime, you can use the following commands.\n\n'
                         '/register - you need to be registered first.\n'
                         '/menu - Minimum set of working functions.\n'
                         '/profile - Get data from database profile.\n'
                         '/ban - Would be banned from working functions.\n'
                         '/unban - Would be returned to active status.')
