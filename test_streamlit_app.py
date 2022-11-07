import pandas as pd
# import pytest
import json
from google_sheets import get_google_sheet
from data_collection import get_x_days_activity
import warnings

# get credentials for api and google sheet source
with open('cred.json') as data_file:
    data = json.load(data_file)
client_id = data['client_id']
client_secret = data['client_secret']
sheet_url = data['sheet_url']


def api_v1():
    warnings.warn(UserWarning("api v1, should use functions from v2"))
    return 1


def test_one():
    assert api_v1() == 1


def test_get_google_sheet():
    result = get_google_sheet(sheet_url, 'PB')

    #  test datatype
    assert isinstance(result, pd.DataFrame)

    # test columns
    assert len(result.axes[1]) == 4


def test_get_x_days_activity():
    result = get_x_days_activity(15, client_id, client_secret)
    #  test datatype
    assert isinstance(result, pd.DataFrame)

    # test columns
    assert len(result.axes[1]) == 5

    # test column names
    assert result.columns.to_list() == \
           [
                 'id'
               , 'Name'
               , 'Start Date'
               , 'Calories'
               , 'Steps'
           ]
