

async def on_startup(dp):

    import filters
    filters.setup(dp)

    import middlewares
    middlewares.setup(dp)

    from loader import db
    from utils.db_api.db_gino import on_startup
    print("Starting Connection to PostrgeSQL...")
    await on_startup(dp)

    # print("Deleting PostrgeSQL...")
    # await db.gino.drop_all()

    print("Creating PostrgeSQL database...")
    await db.gino.create_all()
    print("Connection completed successfully!")

    from utils.db_api.add_to_database import add_leads
    await add_leads()
    print("Новые заявки собраны,\n"
          "Добвлены в базу данных,\n"
          "Oтмечены прочитанными.")

    # from utils.notify_admins import on_startup_notify
    # await on_startup_notify(dp)

    from utils.set_bot_commands import set_default_commands
    await set_default_commands(dp)


    print("Bot Started")

if __name__ == "__main__":
    from aiogram import executor
    from handlers import dp

    executor.start_polling(dp, on_startup=on_startup, skip_updates=True)
