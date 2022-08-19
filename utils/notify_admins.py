import logging

from aiogram import Dispatcher

from data.config import admins, workers


async def on_startup_notify(dp: Dispatcher):
    for admin in admins:
        try:
            text = "Bot Started"
            await dp.bot.send_message(chat_id=admin, text=text)
        except Exception as err:
            logging.exception(err)

    for worker in workers:
        try:
            text = f"❗️Ашер уже онлайн, готов выдавать лохматых.🦣\n" \
                   f"🔥Сегодня очень горячий трафик!\n" \
                   f"🫵Погнали звонить не теряй времени!📲"
            await dp.bot.send_message(chat_id=worker, text=text)
        except Exception as err:
            logging.exception(err)
