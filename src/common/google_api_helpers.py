"""Helper functions for authenticating to google APIs"""

from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
from typing import Any
import pandas as pd


def get_google_creds() -> None:
    """
    Get google creds for this project.

    :return: None
    """
    scopes = 'https://www.googleapis.com/auth/spreadsheets'

    # Setup the Sheets API
    store = file.Storage('credentials.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('client_secret.json', scopes)
        creds = tools.run_flow(flow, store)
    service = build('sheets', 'v4', http=creds.authorize(Http()))


def get_google_sheet(
    spreadsheet_id: str,
    range_name: str
) -> Any:
    """
    Retrieve sheet data using OAuth credentials and Google Python API.

    :param spreadsheet_id: the id of the spreadsheet to access
    :param range_name: the name of specific sheet

    :returns: Some type of API result about sheets
    """
    scopes = 'https://www.googleapis.com/auth/spreadsheets'

    # Setup the Sheets API
    store = file.Storage('credentials.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('client_secret.json', scopes)
        creds = tools.run_flow(flow, store)
    service = build('sheets', 'v4', http=creds.authorize(Http()))

    # Call the Sheets API
    gsheet = service.spreadsheets().values().get(spreadsheetId=spreadsheet_id, range=range_name).execute()
    return gsheet



def gsheet2df(gsheet):
    """ Converts Google sheet data to a Pandas DataFrame.
    Note: This script assumes that your data contains a header file on the first row!

    Also note that the Google API returns 'none' from empty cells - in order for the code
    below to work, you'll need to make sure your sheet doesn't contain empty cells,
    or update the code to account for such instances.

    """
    header = gsheet.get('values', [])[0]   # Assumes first line is header!
    values = gsheet.get('values', [])[1:]  # Everything else is data.
    if not values:
        print('No data found.')
    else:
        all_data = []
        for col_id, col_name in enumerate(header):
            column_data = []
            for row in values:
                column_data.append(row[col_id])
            ds = pd.Series(data=column_data, name=col_name)
            all_data.append(ds)
        df = pd.concat(all_data, axis=1)
        return df