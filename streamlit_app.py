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
lifts_df = get_google_sheet(sheet_url, 'Lifts')

# minor cleaning
# lifts_df = lifts_df.astype(str)
# lifts_df = lifts_df.applymap(lambda s: s.upper() if type(s) == str else s)
lifts_df['Weight'] = lifts_df['Weight'].astype(float)
lifts_df['Reps'] = lifts_df['Reps'].astype(str)
lifts_df['Sets'] = lifts_df['Sets'].astype(int)
lifts_df['Notes'] = lifts_df['Notes'].astype(str)
lifts_df['Day'] = pd.to_datetime(lifts_df['Day'], format='%d/%m/%Y')

# add filter for exercise
Exercises = lifts_df['Exercise'].drop_duplicates()
make_choice = st.sidebar.selectbox('Select your Gym Exercise:', Exercises)
lifts_filt_df = lifts_df.loc[lifts_df["Exercise"] == make_choice]

# create and write graph
c = alt.Chart(lifts_filt_df).mark_line().encode(
     x='Day', y='Weight', color='Reps').properties(width=600, height=300)
st.write(c)

# show base data
st.dataframe(lifts_filt_df)

# fitbit data
st.write('General Activity Table')
# fitbit data
#activity = get_x_days_activity(1, client_id, client_secret)
#activity.to_pickle('activity.pkl')

# add filter for activity
activity_df = pd.read_pickle('activity.pkl')
activity_list = activity_df['Name'].drop_duplicates()
activity_choice = st.sidebar.selectbox('Select your Activity', activity_list)
activity_filt_df = activity_df.loc[activity_df["Name"] == activity_choice]

# create and write graph
st.write('Calories Burnt')
c = alt.Chart(activity_filt_df).mark_bar().encode(
     x='Start Date', y='Calories').properties(width=600, height=300)
st.write(c)

st.write('Steps During Activity')
c = alt.Chart(activity_filt_df).mark_bar().encode(
     x='Start Date', y='Steps').properties(width=600, height=300)
st.write(c)

st.write(activity_filt_df)
