from typing import Union

from aiogram import types
from aiogram.dispatcher.filters import Command

from keyboards.inline.menu_keyboards import categories_keyboard, subcategories_keyboard, leads_keyboard, lead_keyboard, \
    menu_cd
from loader import dp
from utils.db_api.register_lead_commands import get_lead_form


@dp.message_handler(Command('Menu'))
async def show_menu(message: types.Message):
    await list_categories(message)


async def list_categories(message: Union[types.Message, types.CallbackQuery], **kwargs):
    markup = await categories_keyboard()

    if isinstance(message, types.Message):
        await message.answer("Смотри что у нас есть", reply_markup=markup)

    elif isinstance(message, types.CallbackQuery):
        call = message
        await call.message.edit_reply_markup(markup)


async def list_subcategories(callback: types.CallbackQuery, category, **kwargs):
    markup = await subcategories_keyboard(category)
    await callback.message.edit_reply_markup(markup)


async def list_leads(callback: types.CallbackQuery, category, subcategory, **kwargs):
    markup = await leads_keyboard(category=category, subcategory=subcategory)
    await callback.message.edit_text("Смотри, что у нас есть", reply_markup=markup)


async def show_lead(callback: types.CallbackQuery, category, subcategory, lead_id):
    markup = lead_keyboard(category, subcategory, lead_id)

    lead = await get_lead_form(lead_id)
    text = f"Апрув? {lead}"
    await callback.message.edit_text(text, reply_markup=markup)


@dp.callback_query_handler(menu_cd.filter())
async def navigate(call: types.CallbackQuery, callback_data: dict):
    current_level = callback_data.get('level')
    category = callback_data.get('category')
    subcategory = callback_data.get('subcategory')
    lead_id = int(callback_data.get('lead_id'))

    levels = {
        "0": list_categories,
        "1": list_subcategories,
        "2": list_leads,
        "3": show_lead
    }
    current_level_func = levels[current_level]

    await current_level_func(
        call,
        category=category,
        subcategory=subcategory,
        lead_id=lead_id
    )
