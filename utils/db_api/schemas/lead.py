from sqlalchemy import Column, BigInteger, String, sql

from utils.db_api.db_gino import TimedBaseModel


class LeadForm(TimedBaseModel):
    __tablename__ = 'lead_forms'
    query: sql.select

    lead_id = Column(BigInteger, primary_key=True, autoincrement=True)
    create_date = Column(String(50))
    lead_name = Column(String(255))
    phone = Column(String(50))
    email = Column(String(50))
    source = Column(String(100))
    pole_data = Column(String(900))

    status_income = Column(String(25), nullable=True) # created / accepted / invalid
    status_phone = Column(String(25), nullable=True) # answered / not answered
    status_deal = Column(String(50), nullable=True) # deal-comment / not instrested-comment
    status_comment = Column(String(900), nullable=True) # deal-comment / not instrested-comment
    status_alarm = Column(String(100), nullable=True) # deal-comment / not instrested-comment

    def __repr__(self):
        return f"""
ID: {self.lead_id}
Name: {self.lead_name}
Phone: {self.lead_phone}
Source: {self.lead_source}
Pole Data: {self.pole_data}
Date Created: {self.create_date}
"""


