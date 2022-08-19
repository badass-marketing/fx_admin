from sqlalchemy import Column, BigInteger, sql, DateTime, String
from utils.db_api.db_gino import TimedBaseModel


class ChatUser(TimedBaseModel):
    __tablename__ = 'chat_users'
    user_id = Column(BigInteger, primary_key=True)
    first_name = Column(String(255))
    last_name = Column(String(255))
    reputation = Column(BigInteger)
    total_help = Column(BigInteger)
    mutes = Column(BigInteger)
    last_rep_boost = Column(DateTime)
    last_help_boost = Column(DateTime)

    query: sql.select
