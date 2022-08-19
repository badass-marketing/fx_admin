"""
import datetime
from aiogram import types
from asyncpg import UniqueViolationError
from data import config
from loader import bot
from utils.db_api.db_gino import db
from utils.db_api.schemas.chat_actions import ChatAction
from utils.db_api.schemas.chat_user import ChatUser



async def add_chat_user(user_id: int, first_name: str, last_name: str, reputation: int, total_help: int, mutes: int, ):
    try:
        chat_user = ChatUser(user_id=user_id, first_name=first_name, last_name=last_name, reputation=reputation, total_help=total_help, mutes=mutes)
        await chat_user.create()
    except UniqueViolationError:
        print('Регистрация не создана!')


async def check_chat_user(message):
    if message.reply_to_message:
        if await select_chat_user(message.reply_to_message.from_user.id) is None:
            await add_chat_user(user_id=message.reply_to_message.from_user.id,
                                first_name=message.reply_to_message.from_user.first_name,
                                last_name=message.reply_to_message.from_user.last_name,
                                reputation=0,
                                total_help=0,
                                mutes=0,
                                last_rep_boost=datetime.datetime.now() - datetime.timedelta(hours=4),
                                last_help_boost=datetime.datetime.now() - datetime.timedelta(hours=4))
        else:
            pass
    else:
        if await select_chat_user(message.from_user.id) is None:
            await add_chat_user(user_id=message.
                                from_user.id,
                                first_name=message.
                                from_user.first_name,
                                last_name=message.
                                from_user.last_name,
                                reputation=0,
                                total_help=0,
                                mutes=0,
                                last_rep_boost=datetime.datetime.now() - datetime.timedelta(hours=4),
                                last_help_boost=datetime.datetime.now() - datetime.timedelta(hours=4)
        else:
            pass


async def add_chat_action(id: int, user_id: int, type: str):
        try:
            chat_action = ChatAction(id=id, user_id=user_id, type=type, added=datetime.datetime.now())
            await chat_action.create()
        except UniqueViolationError:
            print('Действие из чата не создано в БД')


async def count_user_violations(user_id: int, hours: int = 0):
    violations = await ChatUser.query.where(ChatUser.user_id == user_id).gino.all()
    if hours <= 0:
        return len(violations)
    else:
        count = 0
        for violation in violations:
            if violation.added >= datetime.datetime.now() - datetime.timedelta(hours=hours):
                count += 1
        return count


async def check_violations(message):
    violations = await ChatAction.query.where(ChatAction.user_id == message.from_user.id).gino.all()
    count_bad_words = 0
    count_advertising = 0
    for violation in violations:
        if violation.added >= datetime.datetime.now() - datetime.timedelta(minutes=config.time_of_violations):
            if violation.type == 'bad word':
                count_bad_words += 1
            elif violation.type == 'ads':
                    count_advertising += 1

    OnlyReadPermissions = types.ChatPermissions(can_send_messages=False,
                                                can_send_media_messages=False,
                                                can_send_polls=False,
                                                can_invite_users=False,
                                                can_pin_messages=False,
                                                can_change_info=False,
                                                can_send_other_messages=False,
                                                can_add_web_page_previews=False)
    userChatActions = await ChatAction.query.where(ChatAction.user_id == message.from_user.id).gino.all()
    type = userChatActions[len(userChatActions) - 1].type
    if type == 'bad_word':
        if count_bad_words > 0:
            if count_bad_words >= 5:
                until_date = datetime.datetime.now() + datetime.timedelta(hours=config.mute_by_bad_word_time)
                await bot.restrict_chat_member(chat_id=message.chat.id, user_id=message.from_user.id, permissions=OnlyReadPermissions, until_date=until_date)
                return await message.answer(f"👨‍💻{message.from_user.get_mention(as_html=True)} был ограничен в возможности писать сообщения на {config.mute_by_ads_time} часов.\n"
                                            f"️Причина: Мат в чате!⛔️\n"
                                            f"😡Есть здесь еше желающие?😤")
            else:
                return await message.answaer(f"🤬Замечено плохое слово!\n"
                                             f"Автор х*ни:\ {message.from_user.get_mention(as_html=True)}\'\n"
                                             f"Объявляется предупреждение №{count_bad_words}\n"
                                             f"A warning is issued to the user\n"
                                             f"🫵You already have {count_bad_words} bro...👎")
    elif type == 'ads':
        if count_advertising >=3:
            until_date = datetime.datetime.now() + datetime.timedelta(hours=config.mute_by_ads_time)
            await bot.register_chat_member(chat_id=message.chat_id, user_id=message.from_user.id, permissions=OnlyReadPermissions, until_date=until_date)
            return await message.answer(f"{message.from_user.get_mention(as_html=True)} был ограничен в возможности писать сообщения на {config.mute_by_ads_time} часов.\n"
                                        f"️Причина: Реклама в чате!⛔️\n"
                                        f"😡Есть здесь еше желающие?😤")
        else:
            return await message.answer(f"Замечена реклама в чате!\n"
                                        f"Написал \"{message.from_user.get_mention(as_html=True)}\"\n"
                                        f"🙅‍️Я повторяю еще раз, ненадо здесь ничего рекламировать!🚫\n"
                                        f"Предупреждение № {count_advertising}\n")


async def update_last_help_boost(user_id: int):
    chatuser = await ChatUser.query.where(ChatUser.user_id == user_id).gino.first()
    await chatuser.update(last_help_boost=datetime.datetime.now()).apply()


async def update_last_rep_boost(user_id: int):
    chatuser = await ChatUser.query.where(ChatUser.user_id == user_id).gino.first()
    await chatuser.update(last_rep_boost=datetime.datetime.now()).apply()


async def count_chat_action():
    count = await db.func.count(ChatAction.id).gino.scalar()
    return count


async def select_chat_user(user_id: int):
    chat_user = await ChatUser.query.where(ChatUser.user_id == user_id).gino.first()
    return chat_user


async def add_total_help(user_id: int):
    chat_user = await select_chat_user(user_id)
    await chat_user.update(total_help=chat_user.total_help + 1).apply()


async def add_reputation(user_id: int):
    chat_user = await select_chat_user(user_id)
    await chat_user.update(reputation=chat_user.reputation + 1).apply()


async def remove_reputation(user_id: int):
    chat_user = await select_chat_user(user_id)
    await chat_user.update(reputation=chat_user.reputation - 1).apply()


async def add_mutes(user_id: int):
    chat_user = await select_chat_user(user_id)
    await chat_user.update(mutes=chat_user.mutes + 1).apply()
"""









