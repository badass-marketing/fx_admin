from sqlalchemy import Column, BigInteger, String, sql

from utils.db_api.db_gino import TimedBaseModel


class Registration(TimedBaseModel):
    __tablename__ = 'registrations'
    user_id = Column(BigInteger, primary_key=True)
    tg_first_name = Column(String(250))
    tg_last_name = Column(String(250))
    name = Column(String(100))
    phone = Column(String(15))
    age = Column(String(5))
    status = Column(String(25))

    query: sql.select
