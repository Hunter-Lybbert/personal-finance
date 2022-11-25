"""Tests for helper functions for authenticating to google APIs found in src/common/google_api_helpers.py"""

import os
from pathlib import Path

import pandas as pd

from src.common.google_api_helpers import (
    get_google_creds,
    get_google_sheet,
    get_path_to_google_creds,
    gsheet2df,
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
    SPREADSHEET_ID = "1giRkGWGEw18NYc1b7LhxYvq9eRBF2F-XMJv_i_LG3tE"
    RANGE_NAME = "testing"

    service = get_google_creds("google_creds")
    gsheet = get_google_sheet(
        service=service, spreadsheet_id=SPREADSHEET_ID, range_name=RANGE_NAME
    )
    df = gsheet2df(gsheet=gsheet)
    expected = pd.DataFrame(
        [[2, 3], [4, 5], [6, 7], [8, 9]], columns=["Column 1", "Column 2"]
    )
    print(df, expected, sep="\n")
    print(df.columns == expected.columns)
    print(df.values == expected.values)
    print(df["Column 1"].dtype, expected["Column 1"].dtype)
    assert df.equals(expected)
