from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


ikb_menu_apply = InlineKeyboardMarkup(row_width=2,
                                inline_keyboard=[
                                    [
                                        InlineKeyboardButton(text="Подтвердить", callback_data="accept"),
                                        InlineKeyboardButton(text="Удалить", callback_data='delete')
                                    ]
                                ])

dashboard_menu = InlineKeyboardMarkup(row_width=2,
                                      inline_keyboard=[
                                          [
                                              InlineKeyboardButton(text="")
                                          ]
                                      ])