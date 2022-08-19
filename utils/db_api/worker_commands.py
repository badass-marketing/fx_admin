from typing import List

from asyncpg import UniqueViolationError

from utils.db_api.schemas.lead import LeadForm
from utils.db_api.schemas.sales_manager import Worker


async def add_worker_registration(user_id: int,
                                  first_name: str,
                                  last_name: str,
                                  user_name: str,
                                  worker_age: str,
                                  worker_category: str,
                                  status: str):
    try:
        registration = Worker(user_id=user_id,
                              first_name=first_name,
                              last_name=last_name,
                              user_name=user_name,
                              worker_category=worker_category,
                              status=status,
                              worker_age=worker_age)
        await registration.create()
    except UniqueViolationError:
        print('Регистрация не создана.')


async def select_worker_registration():
    registration = await Worker.query.where(Worker.status == 'created').gino.first()
    return registration


async def select_w_reg_by_userid(user_id: int):
    registration = await Worker.query.where(Worker.user_id == user_id).gino.first()
    return registration


async def accept_w_registration(user_id: int):
    registration = await select_w_reg_by_userid(user_id)
    await registration.update(status='accepted').apply()


async def select_worker(user_id):
    worker = await Worker.query.where(Worker.user_id == user_id).gino.first()
    return worker


async def select_accepted_workers():
    worker = await Worker.query.where(Worker.status == 'accepted').gino.all()
    return worker


async def select_created_workers() -> List[Worker]:
    worker = await Worker.query.where(Worker.status == 'created').gino.all()
    return worker


async def get_workers_online() -> List[Worker]:
    return await Worker.query.where(Worker.status == 'online').gino.all()


async def select_online_workers():
    worker = await Worker.query.where(Worker.status == 'online').gino.all()
    return worker


async def update_worker_status(user_id, status):
    worker = await select_worker(user_id)
    await worker.update(status=status).apply()


async def count_worker_stack(user_id):
    stack = await Worker.query.where(Worker.worker_lead_stack is not None).all()
    return len(stack)


# async def decline_worker(user_id):


# async def add_worker(**kwargs):
#     new_worker = await Worker(**kwargs).create()
#     return new_worker


# async def select_worker_registration():
#     registration = await Worker.query.where(Worker.worker_status == 'created').gino.first()
#     return registration
#
#
# async def select_w_registration_by_userid(user_id: int):
#     registration = await Worker.query.where(Worker.user_id == user_id).gino.first()
#     return registration
#
#
# async def accept_w_registration(user_id: int):
#     registration = await select_w_registration_by_userid(user_id)
#     await registration.update(worker_status='accepted').apply()
#
#
# async def get_worker_category() -> List[Worker]:
#     return await Worker.query.distinct(Worker.worker_category).gino.all()
#
#
# async def get_worker_status() -> List[Worker]:
#     return await Worker.query.distinct(Worker.worker_status).gino.all()
#
#
# # async def get_worker_lead_stack() -> List[LeadForm]:
#
#
# async def get_worker_phone_stats() -> List[Worker]:
#     return await Worker.query.distinct(Worker.worker_phone_stats).gino.all()
#
#
# async def get_worker_deal_stats() -> List[Worker]:
#     return await Worker.query.distinct(Worker.worker_deal_stats).gino.all()
