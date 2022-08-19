from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

kb_worker_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Статус "Онлайн"')
        ]
    ],
    resize_keyboard=True
)

kb_worker_data = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Скрипты отдела продаж')
        ],
[
            KeyboardButton(text='Моя статистика')
        ],
        [
            KeyboardButton(text='[*]SMS Bomber'),
            KeyboardButton(text='Inline Menu')
        ]
    ],
    resize_keyboard=True,
    # one_time_keyboard=True
)

kb_worker_back = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Назад')
        ]
    ],
    resize_keyboard=True
)