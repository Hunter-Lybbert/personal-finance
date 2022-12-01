"""This script will create a new months budget sheet."""

from src.common.google_api_helpers import (
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
# SHEET_ID = 1116040579 if REAL else 1116040579

if __name__ == "__main__":
    sheetIds = [1116040579, 960916036]
    newNames = ["Transactions December", "Summary December"]

    service = get_google_creds(
        creds_directory="google_creds",
        scopes=["https://www.googleapis.com/auth/spreadsheets"],
    )

    for sheetId, newName in zip(sheetIds, newNames):
        response = copy_worksheet(
            service=service,
            spreadsheetId=BUDGET_SPREADSHEET_ID,
            sheetId_to_copy=sheetId,
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
            sheetId=new_sheetId,
        )
