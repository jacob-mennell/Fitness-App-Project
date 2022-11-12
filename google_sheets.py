import pandas as pd
import gspread as gs


def get_google_sheet(sheet_url: str, sheet_name: str) -> pd.DataFrame:
    #sheet_url = os.getenv('sheet_url')

    # authenticate
    gc = gs.service_account(filename='service_account.json')

    # open from url
    sh = gc.open_by_url(sheet_url)

    # select workbook
    sheet = sh.worksheet(sheet_name)

    # create Data Frame
    df = pd.DataFrame(sheet.get_all_records())

    # enforce case
    df = df.applymap(lambda s: s.upper() if type(s) == str else s)

    return df