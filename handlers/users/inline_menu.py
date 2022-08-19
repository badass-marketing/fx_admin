from aiogram import types
from aiogram.types import CallbackQuery

from keyboards.default import kb_test
from loader import dp

from keyboards.inline import ikb_menu_apply, ikb_menu2
from utils.db_api.register_lead_commands import apply_lead_form_margulan, delete_lead_form_margulan


@dp.message_handler(text="Inline Menu")
async def show_inline_menu(message: types.Message):
    await message.answer('Инлайн кнопки ниже', reply_markup=ikb_menu_apply)


@dp.callback_query_handler(text="сообщение")
async def send_message(call: CallbackQuery):
    await call.message.answer('Лидформа подтверждена')


# @dp.callback_query_handler(text="delete")
# async def delete_lead_data(call: CallbackQuery):
#     await delete_lead_form_margulan()
#     # await call.message.edit_reply_markup(ikb_menu2)
#     # await call.message.delete_reply_markup()
#     # await call.message.delete()
#
#
# @dp.callback_query_handler(text="accept")
# async def send_message(call: CallbackQuery):
#     await apply_lead_form_margulan()
#     await call.message.edit_reply_markup(ikb_menu2)
