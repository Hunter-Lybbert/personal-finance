"""
Tests for helper functions for authenticating to google APIs found in src/common/google_api_helpers.py

The url for the sheet used in all the tests is as follows:
https://docs.google.com/spreadsheets/d/1giRkGWGEw18NYc1b7LhxYvq9eRBF2F-XMJv_i_LG3tE/edit#gid=0
"""

import os
import time
from pathlib import Path

import pandas as pd

from src.common.google_api_helpers import (
    clear_values_in_worksheet,
    copy_worksheet,
    create_worksheet,
    delete_worksheet,
    get_google_creds,
    get_google_sheet,
    get_path_to_google_creds,
    gsheet_to_df,
    rename_worksheet,
)


def test_get_path_to_google_creds() -> None:
    """
    Use pathlib to get path to google creds.

    :return: a pathlib.Path object
    """
    creds_dir = "google_creds"
    actual = get_path_to_google_creds(creds_dir)

    relative_path = Path(__file__).parent.parent.parent
    expected = Path(os.path.join(relative_path, creds_dir))

    assert actual == expected


def test_get_google_creds() -> None:
    """
    Test the get_google_creds() function.

    :return: None
    """
    scopes = "https://www.googleapis.com/auth/spreadsheets"
    creds_directory = "google_creds"
    service = get_google_creds(
        creds_directory=creds_directory,
        scopes=scopes,
    )

    SPREADSHEET_ID = "1giRkGWGEw18NYc1b7LhxYvq9eRBF2F-XMJv_i_LG3tE"
    RANGE_NAME = "testing"
    gsheet = get_google_sheet(
        service=service, spreadsheet_id=SPREADSHEET_ID, range_name=RANGE_NAME
    )

    datatypes = {"Name": str, "Pay": float, "Column 1": int, "Column 2": int}
    df = gsheet_to_df(gsheet=gsheet, datatypes=datatypes)

    expected = pd.DataFrame(
        [
            ["Joe", 1.12, 2, 3],
            ["James", 1.01, 4, 5],
            ["Jack", 1.92, 6, 7],
            ["Jane", 1.34, 8, 9],
        ],
        columns=["Name", "Pay", "Column 1", "Column 2"],
    )

    assert df.equals(expected)


def test_delete_worksheet() -> None:
    """
    Test the delete_worksheet() function.

    :return: None
    """
    SPREADSHEET_ID = "1giRkGWGEw18NYc1b7LhxYvq9eRBF2F-XMJv_i_LG3tE"
    sheetId = 7
    service = get_google_creds(
        creds_directory="google_creds",
        scopes=["https://www.googleapis.com/auth/spreadsheets"],
    )
    create_worksheet(
        service=service,
        spreadsheetId=SPREADSHEET_ID,
        sheetId=sheetId,
        new_worksheet_name="testing_delete_function",
    )

    time.sleep(5)

    delete_worksheet(
        service=service,
        spreadsheetId=SPREADSHEET_ID,
        sheetId=sheetId,
    )


def test_create_worksheet() -> None:
    """
    Test the create_worksheet() function.

    :return: None
    """
    SPREADSHEET_ID = "1giRkGWGEw18NYc1b7LhxYvq9eRBF2F-XMJv_i_LG3tE"
    sheetId = 9
    service = get_google_creds(
        creds_directory="google_creds",
        scopes=["https://www.googleapis.com/auth/spreadsheets"],
    )
    create_worksheet(
        service=service,
        spreadsheetId=SPREADSHEET_ID,
        sheetId=sheetId,
        new_worksheet_name="testing_sheet_8",
    )

    time.sleep(5)

    delete_worksheet(
        service=service,
        spreadsheetId=SPREADSHEET_ID,
        sheetId=sheetId,
    )


def test_copy_worksheet() -> None:
    """
    Test the test_create_copy_of_sheet() function.

    :return:
    """
    SPREADSHEET_ID = "1giRkGWGEw18NYc1b7LhxYvq9eRBF2F-XMJv_i_LG3tE"
    sheetId = 1164849594
    service = get_google_creds(
        creds_directory="google_creds",
        scopes=["https://www.googleapis.com/auth/spreadsheets"],
    )

    copy_worksheet(
        service=service,
        spreadsheetId=SPREADSHEET_ID,
        sheetId_to_copy=sheetId,
    )


def test_clear_values_in_worksheet() -> None:
    """
    Test the clear_values_in_worksheet() function.

    :return:
    """
    SPREADSHEET_ID = "1giRkGWGEw18NYc1b7LhxYvq9eRBF2F-XMJv_i_LG3tE"
    sheetId = 81190407
    service = get_google_creds(
        creds_directory="google_creds",
        scopes=["https://www.googleapis.com/auth/spreadsheets"],
    )
    response = clear_values_in_worksheet(
        service=service,
        spreadsheetId=SPREADSHEET_ID,
        sheetId=sheetId,
    )
    assert response is not None


def test_rename_worksheet() -> None:
    """
    Test the rename_worksheet() function.

    :return:
    """
    SPREADSHEET_ID = "1giRkGWGEw18NYc1b7LhxYvq9eRBF2F-XMJv_i_LG3tE"
    newName = "New Name for New Sheet"
    sheetId = 81190407
    service = get_google_creds(
        creds_directory="google_creds",
        scopes=["https://www.googleapis.com/auth/spreadsheets"],
    )
    response = rename_worksheet(
        service=service,
        spreadsheetId=SPREADSHEET_ID,
        sheetId=sheetId,
        newName=newName,
    )
    assert response is not None
