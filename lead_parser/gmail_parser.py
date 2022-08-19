
import os.path
from datetime import datetime
import json
import csv

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from states import LeadAddState

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/gmail.modify']

cur_time = datetime.now().strftime("%Y-%m-%d|%H:%M")


async def get_books_from_gmail_api():
    result = []
    global phone_num
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'lead_parser/credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        # Call the Gmail API
        service = build('gmail', 'v1', credentials=creds)

        results = service.users().messages().list(
            userId='me',
            labelIds=['INBOX'],
            q="is:unread"
        ).execute()

        messages = results.get('messages', [])
        for message in messages:
            msg = service.users().messages().get(
                userId='me',
                id=message['id']
            ).execute()
            source_data = msg['payload']['headers']
            for values in source_data:
                name_part = values['name']
                source_part = values['value']
                if name_part == "From" and source_part in [
                    "noreply@fx24-glypi.fun",
                    "noreply@fx24-pyt-treidera.fun"]:
                    source = values["value"].replace(
                        "noreply",
                        ""
                    ).replace(
                        "@fx24-", ""
                    ).replace(
                        ".fun", ""
                    ).upper()

                    email_data = msg['snippet'].split()
                    date = email_data[1]
                    time = email_data[2]
                    name = email_data[4].upper()
                    mail = email_data[6]
                    for phone_part in email_data[8:10]:
                        phone_num = phone_part.replace(
                            "[",
                            ""
                        ).replace(
                            "]",
                            ""
                        ).replace(
                            "'",
                            ""
                        )
                    array = [date, time, name, mail, phone_num, source]
                    result.append(array)

                    # result.append(
                    #     {
                    #         "date": date,
                    #         "time": time,
                    #         "name": name,
                    #         "mail": mail,
                    #         "phone": phone_num,
                    #         "source": source
                    #     }
                    # )
                    #
                    # with open("storage/result.json", "w") as file:
                    #     json.dump(result, file, indent=4, ensure_ascii=False)

                    with open("lead_parser/storage/result.csv", "w") as file:
                        writer = csv.writer(file)  # delimeter can be present

                        writer.writerow(
                            (
                                'Date',
                                'Time',
                                'Name',
                                'Email',
                                'Phone Number',
                                'Client Source'
                            )
                        )

                        writer.writerows(
                            result
                        )
                    print("[*] - CSV файл с данными клиентов создан успешно!")

    except HttpError as error:
        print(f'An error occurred: {error}')


async def get_margulan():
    result = []
    global phone, pole_data, lead_source
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'lead_parser/credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        # Call the Gmail API
        service = build('gmail', 'v1', credentials=creds)

        results = service.users().messages().list(
            userId='me',
            labelIds=['INBOX'],
            q="is:unread"
        ).execute()
        # print(results)

        messages = results.get('messages', [])
        for message in messages:
            msg = service.users().messages().get(
                userId='me',
                id=message['id']
            ).execute()
            source_data = msg['payload']['headers']
            for values in source_data:
                name_part = values['name']
                source_part = values['value']
                if name_part == "From" and source_part == "noreply@fx24-marg.fun":
                    lead_source = values["value"].replace(
                        "noreply",
                        ""
                    ).replace(
                        "@fx24-", ""
                    ).replace(
                        ".fun", ""
                    ).upper()
                    # result.append(lead_source)
                    # return source

                    for values in source_data:
                        name_part = values['name']
                        source_part = values['value']
                        if name_part == 'Subject':
                            pole_data = source_part.strip()
                            # print(pole_data)
                            # result.append(pole_data)

                    email_data = msg['snippet'].split()
                    # print(len(email_data))
                    # print(f"EMAIL_DATA: {email_data}")
                    date = email_data[1]
                    print(f"date: {date}")
                    time = email_data[2]
                    print(f"time {time}")
                    name = email_data[4].upper()
                    print(f"name {name}")
                    mail = email_data[7]
                    print(f"mail {mail}")

                    for phone_part in email_data[8:10]:
                        phone = phone_part.replace(
                            "[",
                            ""
                        ).replace(
                            "]",
                            ""
                        ).replace(
                            "'",
                            ""
                        )
                    print(f"phone {phone}")
                    print(f"pole {pole_data}")
                    # result.append(phone)
                    array = [date, time, name, mail, phone, pole_data]
                    result.append(array)
                    # result.extend((array, {"date": date, "time": time, "name": name, "mail": mail, "phone": phone, "source": lead_source, "pole": pole_data}))
                    #
                    # with open("storage/result.json", "w") as file:
                    #     json.dump(result, file, indent=4, ensure_ascii=False)

                    with open("lead_parser/storage/result.csv", "w") as file:
                        writer = csv.writer(file)  # delimeter can be present

                        writer.writerow(
                            (
                                'Date',
                                'Time',
                                'Name',
                                'Email',
                                'Phone Number',
                                'Client Source',
                                'Pole Data'
                            )
                        )

                        writer.writerows(
                            result
                        )

                    print("[*] - CSV файл с данными клиентов создан успешно!")

    except HttpError as error:
        print(f'An error occurred: {error}')


async def get_ilon():
    result = []
    global phone, pole_data, lead_source
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'lead_parser/credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        # Call the Gmail API
        service = build('gmail', 'v1', credentials=creds)

        results = service.users().messages().list(
            userId='me',
            labelIds=['INBOX'],
            q="is:unread"
        ).execute()
        # print(results)

        messages = results.get('messages', [])
        for message in messages:
            msg = service.users().messages().get(
                userId='me',
                id=message['id']
            ).execute()
            source_data = msg['payload']['headers']
            for values in source_data:
                name_part = values['name']
                source_part = values['value']
                if name_part == "From" and source_part == "noreply@fx24-ilon.fun":
                    lead_source = values["value"].replace(
                        "noreply",
                        ""
                    ).replace(
                        "@fx24-", ""
                    ).replace(
                        ".fun", ""
                    ).upper()
                    # result.append(lead_source)
                    # return source

                    email_data = msg['snippet'].split()
                    # print(len(email_data))
                    # print(f"EMAIL_DATA: {email_data}")
                    date = email_data[1]
                    print(f"date: {date}")
                    time = email_data[2]
                    print(f"time {time}")
                    name = email_data[4].upper()
                    print(f"name {name}")
                    mail = email_data[7]
                    print(f"mail {mail}")

                    for phone_part in email_data[8:10]:
                        phone = phone_part.replace(
                            "[",
                            ""
                        ).replace(
                            "]",
                            ""
                        ).replace(
                            "'",
                            ""
                        )
                    print(f"phone {phone}")
                    # print(f"pole {pole_data}")
                    # result.append(phone)
                    array = [date, time, name, mail, phone]
                    result.append(array)
                    # result.extend((array, {"date": date, "time": time, "name": name, "mail": mail, "phone": phone, "source": lead_source, "pole": pole_data}))
                    #
                    # with open("storage/result.json", "w") as file:
                    #     json.dump(result, file, indent=4, ensure_ascii=False)

                    with open("lead_parser/storage/result.csv", "w") as file:
                        writer = csv.writer(file)  # delimeter can be present

                        writer.writerow(
                            (
                                'Date',
                                'Time',
                                'Name',
                                'Email',
                                'Phone Number',
                                'Client Source',
                                'Pole Data'
                            )
                        )

                        writer.writerows(
                            result
                        )

                    print("[*] - CSV файл с данными клиентов создан успешно!")

    except HttpError as error:
        print(f'An error occurred: {error}')


def get_all_unread_json():
    global phone_num, pole_data
    result = []
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                '/Users/pax/PycharmProjects/fx24_tg_admin/lead_parser/credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        # Call the Gmail API
        service = build('gmail', 'v1', credentials=creds)

        results = service.users().messages().list(
            userId='me',
            labelIds=['INBOX'],
            q="is:unread"
        ).execute()

        messages = results.get('messages', [])
        for message in messages:
            msg = service.users().messages().get(
                userId='me',
                id=message['id']
            ).execute()
            source_data = msg['payload']['headers']
            for values in source_data:
                name_part = values['name']
                source_part = values['value']
                if name_part == "From" and source_part in [
                    "noreply@fx24-glypi.fun",
                    "noreply@fx24-pyt-treidera.fun",
                    "noreply@fx24-marg.fun",
                    "noreply@fx24-ilon.fun"]:
                    lead_source = values["value"].replace(
                        "noreply",
                        ""
                    ).replace(
                        "@fx24-", ""
                    ).replace(
                        ".fun", ""
                    ).upper()
                    for values in source_data:
                        name_part = values['name']
                        source_part = values['value']
                        if name_part == 'Subject':
                            pole_data = source_part.strip()
                            # print(pole_data)
                            # result.append(pole_data)
                    email_data = msg['snippet'].split()
                    date = email_data[1]
                    time = email_data[2]
                    name = email_data[4].upper()
                    mail = str(email_data[5:7])
                    for phone_part in email_data[8:10]:
                        phone_num = phone_part.replace(
                            "[",
                            ""
                        ).replace(
                            "]",
                            ""
                        ).replace(
                            "'",
                            ""
                        )
                    # array = [date, time, name, mail, phone_num, lead_source, pole_data]
                    # result.append(array)

                    result.append(
                        {
                            "date": date,
                            "time": time,
                            "lead_name": name,
                            "email": mail,
                            "phone": phone_num,
                            "source": lead_source,
                            "pole_data": pole_data
                        }
                    )

                    with open("/Users/pax/PycharmProjects/fx24_tg_admin/lead_parser/storage/result.json", "w") as file:
                        json.dump(result, file, indent=4, ensure_ascii=False)

        print("[*] - JSON serialization файл с данными клиентов создан успешно!")

    except HttpError as error:
        print(f'An error occurred: {error}')


async def check_email(choice_type='y'):
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'lead_parser/credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        # Call the Gmail API
        service = build('gmail', 'v1', credentials=creds)
        # results = service.users().labels().list(userId='me').execute()
        # labels = results.get('labels', [])

        results = service.users().messages().list(
            userId='me',
            labelIds=['INBOX'],
            q="is:unread"
        ).execute()
        if messages := results.get('messages', []):
            message_count = 0
            for message in messages:
                msg = service.users().messages().get(userId='me', id=message['id']).execute()
                message_count = message_count + 1
            print(f"[*] - В вашем ящике {str(message_count)} непрочитанных сообщений(я)")

            new_message_choise = choice_type
            if new_message_choise == "y":
                for message in messages:
                    msg = service.users().messages().get(
                        userId='me',
                        id=message['id']
                    ).execute()
                    source_data = msg['payload']['headers']
                    print(f"SOURCE_DATA:{source_data}")
            else:
                exit()
    except HttpError as error:
        print(f'An error occurred: {error}')


async def mark_as_read():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'lead_parser/credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('gmail', 'v1', credentials=creds)

    results = service.users().messages().list(
        userId='me',
        labelIds=['INBOX'],
        q="is:unread"
    ).execute()
    messages = results.get('messages', [])
    for message in messages:
        service.users().messages().modify(
            userId='me',
            id=message['id'],
            body={'removeLabelIds': ['UNREAD']}
        ).execute()


def main():
    # await get_books_from_gmail_api()
    # await get_margulan()
    mark_as_read()
    get_all_unread_json()


if __name__ == '__main__':
    main()
