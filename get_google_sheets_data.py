import pandas as pd
import gspread as gs
import gspread_dataframe as gd


def google_sheet_auth(sheet_url: str,
                      sheet_name: str,
                      credentials: dict):
    """ Func to authenticate connection"""
    gc = gs.service_account_from_dict(credentials)

    # open from url
    sh = gc.open_by_url(sheet_url)

    # select workbook
    sheet = sh.worksheet(sheet_name)

    return sheet


def get_google_sheet(sheet_url: str,
                     sheet_name: str,
                     credentials: dict) -> pd.DataFrame:
    '''
    :param credentials: google sheet credentials from service_account.json
    :param sheet_url: str
    :param sheet_name: str
    :return: data frame
    '''
    # select workbook
    sheet = google_sheet_auth(sheet_url, sheet_name, credentials)

    # create Data Frame
    df = pd.DataFrame(sheet.get_all_records())

    # enforce case
    df = df.applymap(lambda s: s.upper() if type(s) == str else s)

    return df


def export_to_google_sheets(sheet_url: str,
                            sheet_name: str,
                            df_new: pd.DataFrame,
                            credentials: dict) -> None:
    """
    :param sheet_url: str
    :param sheet_name: str
    :param df_new: pd.DataFrame
    :param credentials: google sheet credentials from service_account.jso
    """
    # select workbook
    sheet = google_sheet_auth(sheet_url, sheet_name, credentials)

    # add rows from df
    df_current = get_google_sheet(sheet_url, sheet_name, credentials)

    # concat new data with existing
    final_df = pd.concat([df_current, df_new], join="outer")

    # clear data
    sheet.clear()

    # add new concat final_df_data
    gd.set_with_dataframe(worksheet=sheet,
                          dataframe=final_df,
                          include_index=False,
                          include_column_header=True,
                          resize=True)
