"""This script will create a new months budget sheet."""

from src.common.google_api_helpers import (
    GridRangeType,
    clear_values_in_worksheet,
    copy_worksheet,
    get_google_creds,
    rename_worksheet,
)

REAL = False
BUDGET_SPREADSHEET_ID = (
    "1IKbun3-lXmarmECjW7jwOVf4FT1r_c_F_Fa1HJqiJsE"
    if REAL
    else "1MT-ViKfZajZ0gZaHQ0aYDFHWU94mBcvUVlj7B_oOcRk"
)

if __name__ == "__main__":
    newNames = ["Transactions December", "Summary December"]
    GridRanges = [
        GridRangeType(1116040579, 4, 80, 1, 9),
        GridRangeType(
            960916036, startRowIndex, endRowIndex, startColumnIndex, endColumnIndex
        ),
    ]
    service = get_google_creds(
        creds_directory="google_creds",
        scopes=["https://www.googleapis.com/auth/spreadsheets"],
    )

    for GridRange, newName in zip(GridRanges, newNames):
        response = copy_worksheet(
            service=service,
            spreadsheetId=BUDGET_SPREADSHEET_ID,
            sheetId_to_copy=GridRange.sheetId,
        )
        new_sheetId: int
        if response is not None:
            new_sheetId = response["sheetId"]
        else:
            raise Exception("Sheet copy not successfully created.")

        response2 = rename_worksheet(
            service=service,
            spreadsheetId=BUDGET_SPREADSHEET_ID,
            sheetId=new_sheetId,
            newName=newName,
        )

        response3 = clear_values_in_worksheet(
            service=service,
            spreadsheetId=BUDGET_SPREADSHEET_ID,
            # TODO Fix the parameters later.
            GridRange=GridRange,
        )
