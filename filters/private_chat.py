from aiogram import types
from aiogram.dispatcher.filters import BoundFilter


class IsPrivate(BoundFilter):
    async def check(self, message: types.Message):
        return message.chat.type == types.ChatType.PRIVATE


# class IsPrivate(BoundFilter):
#     async def check(self, message: types.Message):
#         if message.chat.type != types.ChatType.PRIVATE:
#             await message.answer('Этот функционал работает в личной переписке,\n'
#                                  'тип чата должен быть приватным.\n'
#                                  'В общем, отправь свой запрос мне в личку.😎')
#         else:
#             return message.chat.type == types.ChatType.PRIVATE


# CallbackQuery example for private messages
# class IsPrivate(BoundFilter):
#     async def check(self, call: types.CallbackQuery):
#         return call.message.chat.type == types.ChatType.PRIVATE
