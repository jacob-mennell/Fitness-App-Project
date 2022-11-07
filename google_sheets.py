import pandas as pd
import os
# import pickl
# used to access google drive
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

    return df

# using sheet api waiting for approved scope
# from googleapiclient.discovery import build
# from google_auth_oauthlib.flow import InstalledAppFlow,Flow
# from google.auth.transport.requests import Request
# SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
#
# # set the environment variables
# SHEET_ID = os.getenv('SHEET_ID')
# SHEET_RANGE = 'A1:F14'
#
#
# def sheet_load():
#     '''
#     '''
#     global values_input, service
#     creds = None
#     if os.path.exists('token.pickle'):
#         with open('token.pickle', 'rb') as token:
#             creds = pickle.load(token)
#     if not creds or not creds.valid:
#         if creds and creds.expired and creds.refresh_token:
#             creds.refresh(Request())
#         else:
#             flow = InstalledAppFlow.from_client_secrets_file(
#                 'my_json_file.json', SCOPES) # here enter the name of your downloaded JSON file
#             creds = flow.run_local_server(port=0)
#         with open('token.pickle', 'wb') as token:
#             pickle.dump(creds, token)
#
#     service = build('sheets', 'v4', credentials=creds)
#
#     # Call the Sheets API
#     sheet = service.spreadsheets()
#     result_input = sheet.values().get(spreadsheetId=SHEET_ID,
#                                 range=SHEET_RANGE).execute()
#     values_input = result_input.get('values', [])
#
#     if not values_input and not values_expansion:
#         print('No data found.')
#
#     return pd.DataFrame(values_input[1:], columns=values_input[0])
#
#
# df = sheet_load()