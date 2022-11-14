import numpy as np
import altair as alt
import pandas as pd
import streamlit as st
import os
from google_sheets import get_google_sheet
import cherrypy
import fitbit as fitbit
from gather_keys_oauth2 import OAuth2Server
from data_collection import FitbitAnalysis
import json
import plotly.express as px


# get credentials for api and google sheet source
with open('cred.json') as data_file:
    data = json.load(data_file)
client_id = data['client_id']
client_secret = data['client_secret']
sheet_url = data['sheet_url']

# set streamlit app headers
st.header('Fitness Monitoring App')
st.subheader('Gym Strength Data')
st.write('Gym History Table')

# historical lifts from google sheets
lifts_df = get_google_sheet(sheet_url, 'Lifts')
pb_df = get_google_sheet(sheet_url, 'PB')

# minor cleaning
# lifts_df = lifts_df.astype(str)
lifts_df['Weight'] = lifts_df['Weight'].astype(float)
lifts_df['Reps'] = lifts_df['Reps'].astype(str)
lifts_df['Sets'] = lifts_df['Sets'].astype(int)
lifts_df['Notes'] = lifts_df['Notes'].astype(str)
lifts_df['Day'] = pd.to_datetime(lifts_df['Day'], format='%d/%m/%Y')

# add filter for exercise
# exercise_list_master = lifts_df['Exercise'].drop_duplicates()
make_choice = st.sidebar.selectbox('Select your Gym Exercise:', ['BENCH PRESS', 'SQUAT', 'DEADLIFT'])
st.write('You selected:', make_choice)
lifts_filt_df = lifts_df.loc[lifts_df["Exercise"] == make_choice]

# create and write graph
c = alt.Chart(lifts_filt_df).mark_line(point=alt.OverlayMarkDef(color="white")).encode(
     x='Day', y='Weight', color='Reps').properties(width=600, height=300).configure_point(
    size=150)
st.write(c)

# show base data
st.write('Gym Base Data')
st.dataframe(lifts_filt_df)

# fixed one rep max table
st.write('PB Table')
pb_df['Reps'] = pb_df['Reps'].astype(str)
fig = px.bar(pb_df, x="Exercise", y="Weight", color="Reps", barmode="group")
st.write(fig)
st.dataframe(pb_df)

# fitbit data
st.subheader('General Activity Data')

# fitbit data
#activity = get_x_days_activity(1, client_id, client_secret)
#activity.to_pickle('activity.pkl')

# add filter for activity
# export fitbit data to pkl file
# fitinst = FitbitAnalysis(data['client_id'], data['client_secret'])
# activity = fitinst.get_x_days_activity(30)
# activity.to_pickle('activity.pkl')
activity_df = pd.read_pickle('activity.pkl')
activity_list = activity_df['Name'].drop_duplicates().to_list()
activity_choice = st.sidebar.multiselect('Select your Activity', activity_list)
st.write('You selected:', activity_choice)

if not activity_choice:
    activity_filt_df = activity_df.copy()
else:
    activity_filt_df = activity_df.loc[activity_df["Name"].isin(activity_choice)]

# create and write graph
st.write('Calories Burnt')
# c = alt.Chart(activity_filt_df).mark_bar().encode(
#      x='Start_Date', y='Calories').properties(width=600, height=300)
cal_fig = px.bar(activity_filt_df, x="Start_Date", y="Calories", color='Name', barmode="group")
st.write(cal_fig)

st.write('Steps During Activity')
# c = alt.Chart(activity_filt_df).mark_bar().encode(
#      x='Start_Date', y='Steps').properties(width=600, height=300)
steps_fig = px.bar(activity_filt_df, x="Start_Date", y="Steps", color='Name', barmode="group")
st.write(steps_fig)

st.write('Activity Base Data')
st.write(activity_filt_df)