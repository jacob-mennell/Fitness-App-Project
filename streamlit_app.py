import numpy as np
import altair as alt
import pandas as pd
import streamlit as st
import os
from google_sheets import get_google_sheet
import cherrypy
import fitbit as fitbit
from gather_keys_oauth2 import OAuth2Server
from data_collection import get_x_days_activity

# set the environment variables for fitbit API
client_id = os.getenv('CLIENT_ID')
client_secret = os.getenv('CLIENT_SECRET')

# set streamlit app headers
st.header('test web app prior to loading fitness data')
st.write('Personal Fitness Data Application')
st.write('Gym History Table')

# Test data
df = pd.DataFrame({
     'sessions': [1, 2, 3, 4],
     'weight': [10, 20, 30, 40]
     })

# make df from google sheets data - need to get this working
# sheet_url = os.getenv('sheet_url')
# df = get_google_sheet(sheet_url, 'PB')
# df = df.astype(str)
# test read in correctly
print(df.shape)

# st.write(df)
st.dataframe(df)

# fitbit data
activity = get_x_days_activity(10, client_id, client_secret )
st.dataframe(activity)

# random df
df2 = pd.DataFrame(
     np.random.randn(200, 3),
     columns=['a', 'b', 'c'])

# random graph
c = alt.Chart(df2).mark_circle().encode(
     x='a', y='b', size='c', color='c', tooltip=['a', 'b', 'c'])
st.write(c)

