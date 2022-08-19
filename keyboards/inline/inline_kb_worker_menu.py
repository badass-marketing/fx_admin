from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


ikb_menu2 = InlineKeyboardMarkup(row_width=2,
                                inline_keyboard=[
                                    [
                                        InlineKeyboardButton(text="Сообщение", callback_data="сообщение"),
                                        InlineKeyboardButton(text="Ссылка на наш сайт", url='https://tradefx24.net/')
                                    ]
                                ])