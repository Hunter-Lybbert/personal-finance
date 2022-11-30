"""Helper functions for authenticating to google APIs"""

import os
from pathlib import Path
from typing import Any, Union

import pandas as pd
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import client, file, tools

API_SERVER_NAME = "sheets"
API_VERSION = "v4"
DEFAULT_CREDENTIALS_FILE = "credentials.json"
CREDENTIALS_FILE = "client_secret.json"


def get_path_to_google_creds(creds_directory: str) -> Path:
    """
    Use pathlib to get path to google creds.

    :param creds_directory: directory that the Google api credits are saved in

    :return: a pathlib.Path object
    """
    relative_path = Path(__file__).parent.parent.parent
    full_path = os.path.join(relative_path, creds_directory)
    return Path(full_path)


def get_google_creds(
    creds_directory: str,
    scopes: Union[list[str], str],
) -> Any:
    """
    Get google creds for this project.

    :param creds_directory: directory that the Google api credits are saved in
    :param scopes:

    :return: Google API credential results
    """
    full_path = get_path_to_google_creds(creds_directory=creds_directory)

    # Set up the Sheets API
    store = file.Storage(filename=os.path.join(full_path, DEFAULT_CREDENTIALS_FILE))
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets(
            filename=os.path.join(full_path, CREDENTIALS_FILE),
            scope=scopes,
        )
        creds = tools.run_flow(flow, store)
    service = build(API_SERVER_NAME, API_VERSION, http=creds.authorize(Http()))
    return service


def get_google_sheet(
    service: Any,
    spreadsheet_id: str,
    range_name: str,
) -> Any:
    """
    Retrieve sheet data using OAuth credentials and Google Python API.

    :param service: Dictionary of result from authenticating to google API.
    :param spreadsheet_id: the id of the spreadsheet to access
    :param range_name: the name of specific sheet

    :returns: Some type of API result about sheets
    """

    # Call the Sheets API
    gsheet = (
        service.spreadsheets()
        .values()
        .get(spreadsheetId=spreadsheet_id, range=range_name)
        .execute()
    )
    return gsheet


def gsheet_to_df(
    gsheet: Any,
    datatypes: dict[str, Any],
) -> pd.DataFrame:
    """
    Convert data from a Google spreadsheet to Pandas DataFrame.

    :param gsheet: the result of the gsheet query and execution
    :param datatypes: A dictionary of

    :return: pd.DataFrame of the gsheet data
    """
    gsheet_data = gsheet.get("values")
    df = pd.DataFrame(
        data=gsheet_data[1:],
        columns=gsheet_data[0],
    ).astype(dtype=datatypes)
    return df


def copy_worksheet(
    service: Any,
    spreadsheetId: str,
    sheetId_to_copy: int,
) -> dict[Any, Any]:
    """
    Create a copy of an existing sheet in the specified spreadsheet.

    :param service: Dict of Spreadsheet Authentication data
    :param spreadsheetId: the id of the spreadsheet to copy new worksheet in
    :param sheetId_to_copy: the integer for the specific sheet to copy

    :return:
    """
    request_body = {
        "destination_spreadsheet_id": spreadsheetId,
    }
    request = (
        service.spreadsheets()
        .sheets()
        .copyTo(spreadsheetId=spreadsheetId, sheetId=sheetId_to_copy, body=request_body)
    )
    return request.execute()


def create_worksheet(
    service: Any,
    spreadsheetId: str,
    sheetId: int,
    new_worksheet_name: str,
) -> None:
    """
    Create a new worksheet inside an existing spreadsheet.

    :param service: Dict of Spreadsheet Authentication data
    :param spreadsheetId: the id of the spreadsheet to create new worksheet in
    :param sheetId: an integer associated with the specific worksheet  (it's in the url)
    :param new_worksheet_name: name for the new worksheet

    :return: None
    """
    # TODO Catch errors for invalid worksheet names and so on.
    sheet_properties = {
        "title": new_worksheet_name,
        "sheetId": sheetId,
        # TODO decide what properties we need to include.
    }
    add_sheet_request = {"properties": sheet_properties}
    request_body = {"requests": [{"addSheet": add_sheet_request}]}

    spreadsheets = service.spreadsheets()
    spreadsheets.batchUpdate(
        spreadsheetId=spreadsheetId,
        body=request_body,
    ).execute()


def delete_worksheet(
    service: Any,
    spreadsheetId: str,
    sheetId: int,
) -> None:
    """
    Delete a specific worksheet from a given Spreadsheet.

    :param service: Dict of Spreadsheet Authentication data
    :param spreadsheetId: the id of the spreadsheet to create new worksheet in
    :param sheetId: an integer associated with the specific worksheet (it's in the url)

    :return: None
    """
    # TODO Catch errors for invalid worksheet sheetId's and so on.
    delete_request = {"sheetId": sheetId}
    request_body = {"requests": [{"deleteSheet": delete_request}]}
    spreadsheets = service.spreadsheets()
    spreadsheets.batchUpdate(
        spreadsheetId=spreadsheetId,
        body=request_body,
    ).execute()
