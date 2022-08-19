import asyncio
import json

from loader import db
from lead_parser.gmail_parser import get_all_unread_json, mark_as_read
from utils.db_api.register_lead_commands import add_lead_form


async def add_leads():

    get_all_unread_json()

    with open("/Users/pax/PycharmProjects/fx24_tg_admin/lead_parser/storage/result.json") as file:
        forms_data = json.load(file)
        print(forms_data)

    for form_data in forms_data:

        # await form_data.add_lead_form()
        await add_lead_form(lead_name=form_data['lead_name'],
                            create_date=form_data['date'],
                            phone=form_data['phone'],
                            email=form_data['email'],
                            source=form_data['source'],
                            pole_data=form_data['pole_data'],
                            status_income='created'
                            )

    # await mark_as_read()


# loop = asyncio.get_event_loop()
# loop.run_until_complete(add_leads())
