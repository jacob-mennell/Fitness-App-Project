import numpy as np
import altair as alt
import pandas as pd
import streamlit as st
import os
from google_sheets import get_google_sheet
import cherrypy
import fitbit as fitbit
from gather_keys_oauth2 import OAuth2Server
#from data_collection import get_x_days_activity
import json


# get credentials for api and google sheet source
with open('cred.json') as data_file:
    data = json.load(data_file)
client_id = data['client_id']
client_secret = data['client_secret']
sheet_url = data['sheet_url']

# set streamlit app headers
st.header('Fitness Monitoring App')
st.write('Personal Fitness Data Application')
st.write('Gym History Table')

# historical lifts from google sheets
df = get_google_sheet(sheet_url, 'Lifts')
df = df.astype(str)
st.dataframe(df)

# fitbit data
st.write('Gym Activity Table')
# fitbit data
#activity = get_x_days_activity(1, client_id, client_secret)
#activity.to_pickle('activity.pkl')

activity_df = pd.read_pickle('activity.pkl')
st.write(activity_df)
