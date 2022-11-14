import pandas as pd
import pytest
import json
from google_sheets import get_google_sheet
from data_collection import FitbitAnalysis
import warnings

# define scope for pytest.fixture
scope = 'session'


def api_v1():
    warnings.warn(UserWarning("api v1, should use functions from v2"))
    return 1


def test_one():
    assert api_v1() == 1


@pytest.fixture(scope=scope)
def get_cred():
    with open('cred.json') as data_file:
        data = json.load(data_file)
    return data


@pytest.fixture(scope=scope)
def shared_instance(get_cred):
    fitinst = FitbitAnalysis(get_cred['client_id'], get_cred['client_secret'])
    yield fitinst


def test_get_google_sheet(get_cred):
    result = get_google_sheet(get_cred['sheet_url'], 'PB')

    #  test datatype
    assert isinstance(result, pd.DataFrame)

    # test columns
    assert len(result.axes[1]) == 4


def test_get_x_days_activity(shared_instance):
    result = shared_instance.get_x_days_activity(10)

    #  test datatype
    assert isinstance(result, pd.DataFrame)

    # test columns
    assert len(result.axes[1]) == 5

    # test column names
    assert result.columns.to_list() == \
           [
               'id',
               'Name',
               'Start_Date',
               'Calories',
               'Steps']
