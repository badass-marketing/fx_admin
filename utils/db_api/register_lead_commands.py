from typing import List

from asyncpg import UniqueViolationError
from sqlalchemy import and_

from utils.db_api.db_gino import db
from utils.db_api.schemas.lead import LeadForm

from aiogram.types import CallbackQuery


async def new_lead_registration(lead_name: str,
                                phone: str,
                                email: str,
                                source: str,
                                pole_data: str,
                                status: str):
    try:
        lead_registration = LeadForm(lead_name=lead_name,
                                     phone=phone,
                                     email=email,
                                     source=source,
                                     pole_data=pole_data,
                                     status=status)

        await lead_registration.create()
    except UniqueViolationError:
        print("Лид форма не создана.")


async def select_all_glypi():
    lead_registration = await LeadForm.query.where(LeadForm.source == 'GLYPI').gino.all()
    return lead_registration


async def select_all_ilon():
    lead_registration = await LeadForm.query.where(LeadForm.source == 'ILON').gino.first()
    return lead_registration


async def select_all_margulan():
    lead_registration = await LeadForm.query.where(LeadForm.source == 'MARG').gino.first()
    return lead_registration


async def select_lead_registration():
    lead_registration = await LeadForm.query.where(LeadForm.status == 'created').gino.first()
    return lead_registration


async def select_lead_registration_by_lead_id(lead_id: int):
    lead_registration = await LeadForm.query.where(LeadForm.lead_id == lead_id).gino.first()
    return lead_registration


async def accept_lead_registration(lead_id: int):
    lead_registration = await select_lead_registration_by_lead_id(lead_id)
    await lead_registration.update(status='accepted').apply()


async def apply_lead_form_margulan():
    lead_registration = await select_all_margulan()
    await lead_registration.update(status='accepted').apply()


async def delete_lead_form_margulan():
    lead_registration = await select_all_margulan()
    await lead_registration.delete()

# =============================================================================
# ===============New lead form functions =================================================================


async def add_lead_form(**kwargs):
    new_lead = await LeadForm(**kwargs).create()
    return new_lead


async def get_lead_categories() -> List[LeadForm]:
    return await LeadForm.query.distinct(LeadForm.category_code).gino.all()


async def get_lead_subcategories(category) -> List[LeadForm]:
    return await LeadForm.query.distinct(LeadForm.subcategory_code).where(LeadForm.category_code == category).gino.all()


async def count_leads(category_code, subcategory_code=None):
    conditions = [LeadForm.category_code == category_code]

    if subcategory_code:
        conditions.append(LeadForm.subcategory_code == subcategory_code)

    total_leads = await db.select([db.func.count()]).where(
        and_(*conditions)
    ).gino.scalar()
    return total_leads


async def get_lead_form_subcategories(category_code, subcategory_code) -> List[LeadForm]:
    leads = await LeadForm.query.where(
        and_(LeadForm.category_code == category_code,
             LeadForm.subcategory_code == subcategory_code)
    ).gino.all()
    return leads


async def get_lead_form(lead_id) -> LeadForm:
    lead = await LeadForm.query.where(LeadForm.lead_id==lead_id).gino.first()
    return lead



