import pandas as pd
import os
import pytest
from google_sheets import get_google_sheet


def test_get_google_sheet():
    sheet_url = os.getenv('sheet_url')
    result = get_google_sheet(sheet_url, 'PB')
    assert isinstance(result, pd.DataFrame)
