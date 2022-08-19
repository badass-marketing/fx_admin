from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

kb_start = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='/register'),
            KeyboardButton(text='/help')
        ]
    ],
    resize_keyboard=True
)
