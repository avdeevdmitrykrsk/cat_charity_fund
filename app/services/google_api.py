import copy
from datetime import datetime

from aiogoogle import Aiogoogle

from app.core.config import settings


FORMAT = "%Y/%m/%d %H:%M:%S"
PERMISSIONS_BODY = {
    'type': 'user',
    'role': 'writer',
    'emailAddress': settings.email
}

ROW_COUNT = 100
COLUMN_COUNT = 11
SPREADSHEETS_BODY = {
    'properties': {
        'title': 'title',
        'locale': 'ru_RU'
    },
    'sheets': [
        {
            'properties': {
                'sheetType': 'GRID',
                'sheetId': 0,
                'title': 'Лист1',
                'gridProperties': {
                    'rowCount': ROW_COUNT,
                    'columnCount': COLUMN_COUNT
                }
            }
        }
    ]
}


async def spreadsheets_create(
        wrapper_services: Aiogoogle,
        spreadsheet_body=None,
) -> str:
    if spreadsheet_body is None:
        spreadsheet_body = copy.deepcopy(SPREADSHEETS_BODY)
        now_date_time = datetime.now().strftime(FORMAT)
        spreadsheet_body['properties']['title'] = f'Отчёт на {now_date_time}'

    service = await wrapper_services.discover('sheets', 'v4')
    response = await wrapper_services.as_service_account(
        service.spreadsheets.create(json=spreadsheet_body)
    )
    spreadsheetid = response['spreadsheetId']
    return spreadsheetid


async def set_user_permissions(
        spreadsheetid: str,
        wrapper_services: Aiogoogle
) -> None:
    service = await wrapper_services.discover('drive', 'v3')
    await wrapper_services.as_service_account(
        service.permissions.create(
            fileId=spreadsheetid,
            json=PERMISSIONS_BODY,
            fields="id"
        )
    )


async def spreadsheets_update_value(
        spreadsheetid: str,
        projects: list,
        wrapper_services: Aiogoogle
) -> None:
    now_date_time = datetime.now().strftime(FORMAT)
    service = await wrapper_services.discover('sheets', 'v4')
    table_values = [
        ['Отчёт от', now_date_time],
        ['Топ проектов по скорости закрытия'],
        ['Название проекта', 'Время сбора', 'Описание']
    ]
    for project in projects:
        day_str = 'day'
        delta = project.close_date - project.create_date
        if delta.days > 1:
            day_str = 'days'

        days, remainder = divmod(delta.seconds, 86400)
        hours, remainder = divmod(remainder, 3600)
        minutes, seconds = divmod(remainder, 60)
        microseconds = delta.microseconds

        days_format = (
            f'{days} {day_str}, '
            f'{hours:02}:{minutes:02}:{seconds:02}.{microseconds:06}'
        )

        new_row = [project.name, days_format, project.description]
        table_values.append(new_row)

    update_body = {
        'majorDimension': 'ROWS',
        'values': table_values
    }
    await wrapper_services.as_service_account(
        service.spreadsheets.values.update(
            spreadsheetId=spreadsheetid,
            range='A1:E30',
            valueInputOption='USER_ENTERED',
            json=update_body
        )
    )
