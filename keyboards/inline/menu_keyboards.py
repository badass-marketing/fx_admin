from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

from utils.db_api.register_lead_commands import get_lead_categories, count_leads, get_lead_subcategories, get_lead_form

menu_cd = CallbackData("show_menu", "level", "category", "subcategory")
apply_item = CallbackData("apply_item")
delete_item = CallbackData("delete_item")


def make_callback_data(level, category="0", subcategory="0"):
    return menu_cd.new(level=level,
                       category=category,
                       subcategory=subcategory
                       )


async def categories_keyboard():
    CURRENT_LEVEL = 0
    markup = InlineKeyboardMarkup()

    categories = await get_lead_categories()
    for category in categories:
        number_of_items = await count_leads(category.category_code)
        button_text = f"{category.category_name}({number_of_items} голов.)"
        callback_data = make_callback_data(level=CURRENT_LEVEL+1,
                                           category=category.category_code)
        markup.insert(
            InlineKeyboardButton(text=button_text, callback_data=callback_data)
        )

    return markup


async def subcategories_keyboard(category):
    CURRENT_LEVEL = 1
    markup = InlineKeyboardMarkup()

    subcategories = await get_lead_subcategories(category)
    for subcategory in subcategories:
        number_of_items = await count_leads(category_code=category,
                                            subcategory_code=subcategory.subcategory_code)
        button_text = f"{subcategory.subcategory_name}({number_of_items} голов.)"
        callback_data = make_callback_data(level=CURRENT_LEVEL+1,
                                           category=category,
                                           subcategory=subcategory.subcategory_code)
        markup.insert(
            InlineKeyboardButton(text=button_text, callback_data=callback_data)
        )

    markup.row(
        InlineKeyboardButton(
            text="Назад",
            callback_data=make_callback_data(level=CURRENT_LEVEL-1)
        )
    )
    return markup


async def leads_keyboard(category, subcategory):
    CURRENT_LEVEL = 2
    markup = InlineKeyboardMarkup(row_width=1)

    lead_forms = await get_lead_form(lead_id)

    for lead_form in lead_forms:
        button_text = f"{lead_form.name}{lead_form.lead_id}"
        callback_data = make_callback_data(level=CURRENT_LEVEL+1,
                                           category=category,
                                           subcategory=subcategory
                                           )
        markup.insert(
            InlineKeyboardButton(text=button_text, callback_data=callback_data)
        )

    markup.row(
        InlineKeyboardButton(
            text="Назад",
            callback_data=make_callback_data(level=CURRENT_LEVEL-1,
                                             category=category)
        )
    )
    return markup


def lead_keyboard(category, subcategory, lead_id):
    CURRENT_LEVEL = 3
    markup = InlineKeyboardMarkup()
    markup.row(
        InlineKeyboardButton(text="Подтвердить",
                             callback_data=apply_item.new(lead_id=lead_id))
    )
    markup.row(
        InlineKeyboardButton(text="Отклонить",
                             callback_data=delete_item.new(lead_id=lead_id))
    )
    markup.row(
        InlineKeyboardButton(text="Назад", callback_data=make_callback_data(level=CURRENT_LEVEL - 1,
                                                                            category=category,
                                                                            subcategory=subcategory))
    )
    return markup
