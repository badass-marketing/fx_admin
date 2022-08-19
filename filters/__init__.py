from aiogram import Dispatcher

from .private_chat import IsPrivate
from .groups_chat import IsGroup
from .group_admin import IsAdmin


def setup(dp: Dispatcher):
    dp.filters_factory.bind(IsPrivate)
    dp.filters_factory.bind(IsGroup)
    dp.filters_factory.bind(IsAdmin)
