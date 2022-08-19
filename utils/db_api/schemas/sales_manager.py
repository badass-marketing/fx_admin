from sqlalchemy import Column, BigInteger, String, sql

from utils.db_api.db_gino import TimedBaseModel


class Worker(TimedBaseModel):
    __tablename__ = 'managers'
    query: sql.select

    user_id = Column(BigInteger, primary_key=True)
    first_name = Column(String(200))
    last_name = Column(String(200))
    user_name = Column(String(50))
    worker_age = Column(String(30))
    worker_category = Column(String(50)) # sales retention team-lead admin

    status = Column(String(30)) # active / inactive / created
    worker_lead_stack = Column((BigInteger), nullable=True) # quantity of income leads
    worker_phone_stats = Column((BigInteger), nullable=True) # quantity of active phone calls
    worker_deal_stats = Column((BigInteger), nullable=True) # quantity of deals created
    worker_alerts = Column((BigInteger), nullable=True) # quantity of worker alerts
    # TODO: track call time of workers

    def __repr__(self):
        return f"""
Менеджер ID: {self.user_id}
Имя: {self.first_name}
Никнейм: {self.user_name}
Категория: {self.worker_category}
Статус: {self.status}
"""

