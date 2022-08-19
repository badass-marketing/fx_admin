from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

kb_admin_start = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Получить данные'),
        ],
        [
            KeyboardButton(text='Мой SuiSquad'),
            KeyboardButton(text='Мой Лид Хаб')
        ]
    ],
    resize_keyboard=True
)

kb_admin_squad = ReplyKeyboardMarkup(
    [
        [
            KeyboardButton(text='Просмотреть очередь в улей')
        ],
        [
            KeyboardButton(text='Просмотреть пчел "онлайн"')
        ],
        [
            KeyboardButton(text='Назад')
        ]
    ],
    resize_keyboard=True
)

kb_admin_data = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Выгрузить все непрочитанные'),
        ],
        [
            KeyboardButton(text='Отметить прочитанными')
        ],
        [
            KeyboardButton(text='Назад')
        ]
    ],
    resize_keyboard=True,
    # one_time_keyboard=True
)

kb_apply = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Отметить прочитанными')
        ],
        [
            KeyboardButton(text='Назад')
        ]
    ],
    resize_keyboard=True
)

kb_admin_hub = ReplyKeyboardMarkup(
    [
        [
            KeyboardButton(text='Подтвердить новые заявки')
        ],
        [
            KeyboardButton(text='Получить подтвержденные')
        ],
        [
            KeyboardButton(text='Назад')
        ]
    ],
    resize_keyboard=True
)