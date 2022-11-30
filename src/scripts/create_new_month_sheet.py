"""This script will create a new months budget sheet."""

from src.common.google_api_helpers import copy_worksheet, get_google_creds

BUDGET_SPREADSHEET_ID = "1IKbun3-lXmarmECjW7jwOVf4FT1r_c_F_Fa1HJqiJsE"

if __name__ == "__main__":
    sheetId = 1116040579
    service = get_google_creds(
        creds_directory="google_creds",
        scopes=["https://www.googleapis.com/auth/spreadsheets"],
    )
    copy_worksheet(
        service=service,
        spreadsheetId=BUDGET_SPREADSHEET_ID,
        sheetId_to_copy=sheetId,
    )
