
"""
import asyncio
import datetime
import re

from aiogram import types
from aiogram.dispatcher.filters import Command
from aiogram.types import Message
from aiogram.utils.exceptions import BadRequest

from data import config
from filters import IsGroup, IsAdmin
from loader import dp, bot
from utils.db_api import moderator_commands
from utils.misc import rate_limit



@dp.message_handler(IsGroup(), Command('mute', prefixes='!'), IsAdmin())
async def mute_chat_member(message: Message):
    if message.reply_to_message:
        member_id = message.reply_to_message.from_user.id
        chat_id = message.chat.id
        OnlyReadPermissions = types.ChatPermissions(can_send_messages=False,
                                                    can_send_media_messages=False,
                                                    can_send_polls=False,
                                                    can_send_other_messages=False,
                                                    can_add_web_page_previews=False,
                                                    can_change_info=False,
                                                    can_invite_users=False,
                                                    can_pin_messages=False)
        command = re.compile(r"(!mute) ?(\d+)? ?([a-zA-Zа-яА-Я ]+)?").match(message.text)
        time = command.group(2)
        comment = command.group(3)
        if not time:
            time = 30
        else:
            time = int(time)
        until_date = datetime.datetime.now() + datetime.timedelta(minutes=time)
        try:
            await bot.restrict_chat_member(chat_id=chat_id, user_id=member_id, permissions=OnlyReadPermissions, until_date=until_date)
            await message.reply(f"🔇{message.reply_to_message.from_user.get_mention(as_html=True)} был ограничен в возможности отправлять сообщения на {time} минут.\n"
                                f"💬Причине: {comment}")
        except BadRequest:
            await message.reply('🚫Этому пользователю нельзя ограничить возможность отправки сообщений!')
    else:
        msg = await message.reply('❌Эта команда работает только в ответ на сообщение!')
        await asyncio.sleep(15)
        await msg.delete()



@dp.message_handler(IsGroup(), Command('unmute', prefixes='!'), IsAdmin())
async def mute_chat_member(message: Message):
    if message.reply_to_message:
        member_id = message.reply_to_message.from_user.id
        chat_id = message.chat.id
        chat_permissions = (await bot.get_chat(message.chat.id)).permissions
        try:
            await bot.restrict_chat_member(chat_id=chat_id, user_id=member_id, permissions=chat_permissions, until_date=datetime.datetime.now())
            await message.reply(f'🔊{message.from_user.get_mention(as_html=True)} размутил {message.reply_to_message.from_user.get_mention(as_html=True)}')
        except BadRequest:
            await message.reply('❌Этого пользователя нельзя размутить.')
    else:
        msg = await message.reply('❌Эта команда работает только в ответ на сообщение!')
        await asyncio.sleep(15)
        await msg.delete()



@rate_limit(limit=0, key='groups')
@dp.message_handler(IsGroup())
async def moderator(message: Message):
    text = message.text
    await moderator_commands.check_chat_user(message)

    if message.html_text == '/info':
        if message.reply_to_message is None:
            chatUser = await moderator_commands.select_chat_user(message.from_user.id)
            count_Violations = await moderator_commands.count_user_violations(message.from_user.id, hours=24 * 30)
            await message.reply(f'📊Статистика {message.from_user.get_mention(as_html=True)}\n'
                                f'😇Репутация: {chatUser.reputation}\n'
                                f'🛟Всего помощи: {chatUser.total_help}\n'
                                f'🔇Количество мутов: {chatUser.mutes}\n'
                                f'🚫Количество нарушений за последние 30 дней: {count_Violations}')
        else:
            chatUser = await moderator_commands.select_chat_user(message.reply_to_message.from_user.id)
            count_Violations = await moderator_commands.count_user_violations(message.reply_to_message.from_user.id, )
            await message.reply(f'📊Статистика {message.from_user.get_mention(as_html=True)}\n'
                                f'😇Репутация: {chatUser.reputation}\n'
                                f'🛟Всего помощи: {chatUser.total_help}\n'
                                f'🔇Количество мутов: {chatUser.mutes}\n'
                                f'🚫Количество нарушений за последние 30 дней: {count_Violations}'))
    elif message.html_text == '+rep':

            if message.reply_to_message:

                if message.reply_to_message.from_user.id == message.from_user.id:


                    await message.reply("🚫Ты не моежшь поднимать репутацию сам себе.")
                else:
                    chatUser = await moderator_commands.select_chat_user(message.from_user.id)
                    rep_boost_user = await moderator_commands.select_chat_user(message.reply_to_message.from_user.id)
                    if chatUser.last_rep_boost <= datetime.datetime.now() -datetime.timedelta(hours=0.5):
                        await  moderator_commands.update_last_rep_boost(message.from_user.id)
                        await moderator_commands.add_reputation(message.reply_to_message.from_user.id)
                        await moderator_commands.add_chat_action(id=await moderator_commands.count_chat_action() + 1,
                                                                user_id=message.from_user.id,
                                                                type='rep boost')

"""







