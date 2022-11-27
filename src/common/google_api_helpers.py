"""Helper functions for authenticating to google APIs"""

import os
from pathlib import Path
from typing import Any, Union

import pandas as pd
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import client, file, tools

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
    service = build("sheets", "v4", http=creds.authorize(Http()))
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
