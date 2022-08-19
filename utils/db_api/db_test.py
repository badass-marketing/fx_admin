import asyncio

# from data import config
#
# from gino.schema import GinoSchemaVisitor
# from utils.db_api import quick_commands as commands, add_to_database
# from utils.db_api import register_lead_commands as lead_commands
# from utils.db_api.db_gino import db
#
# from data import config
#
#
# async def create_db():
#     await db.set_bind(config.POSTGRES_URL)
#     db.gino: GinoSchemaVisitor
#     await db.gino.create_all()
#
#



# async def db_test():
#     await db.set_bind(config.POSTGRES_URL)
#     # await db.gino.drop_all()
#     await db.gino.create_all()
#
#     await commands.add_user(1, 'Andrey', 'Net')
#     await commands.add_user(6134, 'ddd', 'New name')
#     await commands.add_user(123, 'Ivan', '555')
#     await commands.add_user(8, 'Aleksandr', 'Description')
#     await commands.add_user(984265, 'Vlad', 'd4')
#
#     users = await commands.select_all_users()
#     print(len(users))
#
#     count = await commands.count_users()
#     print(count)
#
#     user = await commands.select_user(1)
#     print(user)
#
#     await commands.update_username(984265, '777Another Vlad')
#
#     user = await commands.select_user(1)
#     print(user)

loop = asyncio.get_event_loop()
loop.run_until_complete(db_test())
