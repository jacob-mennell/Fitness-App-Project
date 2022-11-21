import numpy as np
import altair as alt
import pandas as pd
import streamlit as st
import os
from get_google_sheets_data import get_google_sheet, export_to_google_sheets
import datetime
import plotly.express as px
import plotly.figure_factory as ff


def add_dfForm():
    """
    :rtype: object
    """
    row = pd.DataFrame({'Day': [st.session_state.input_date],
                        'Exercise': [st.session_state.input_exercise],
                        'Weight': [st.session_state.input_weight],
                        'Reps': [st.session_state.input_reps],
                        'Sets': [st.session_state.input_sets]})
    st.session_state.data = pd.concat([st.session_state.data, row])


# using st.secrets
sheet_url = st.secrets['SHEET_URL']
google_sheet_cred_dict = st.secrets['GOOGLE_SHEET_CRED']

############################## streamlit app #############################

# set streamlit app headers
st.header('Fitness Monitoring App')
st.write('App looks at Gym Performance and Fitbit Activity over user defined period')

# input new data
st.write('Add Data to the App')
if 'data' not in st.session_state:
    data = pd.DataFrame({'Day': [], 'Exercise': [], 'Weight': [], 'Reps': [], 'Sets': [], 'Notes': []})
    st.session_state.data = data

data = st.session_state.data

dfForm = st.form(key='dfForm')
with dfForm:
    dfColumns = st.columns(4)
    with dfColumns[0]:
        st.date_input('Day', key='input_date')
    with dfColumns[1]:
        st.selectbox('Exercise', ['BENCH PRESS', 'SQUAT', 'DEADLIFT'], key='input_exercise')
    with dfColumns[2]:
        st.number_input('Weight', key='input_weight', min_value=1, max_value=200, value=100, step=1)
    with dfColumns[3]:
        st.number_input('Reps', key='input_reps',min_value=1, max_value=20, value=8, step=1)
    with dfColumns[3]:
        st.number_input('Sets', key='input_sets',min_value=1, max_value=5, value=3, step=1)
    with dfColumns[3]:
        st.text_input('Notes', key='input_notes')
    st.form_submit_button(on_click=add_dfForm)

# send data back to Google Sheets for storage
export_to_google_sheets(sheet_url=sheet_url, df_new=data, credentials=google_sheet_cred_dict, sheet_name='Lifts')

################### historical lifts from google sheets ##################
# data soon to read directly from SQL

# set headers
st.subheader('Gym Strength Data')
st.write('Gym History Table')

# get data using gspread
lifts_df = get_google_sheet(sheet_url=sheet_url, credentials=google_sheet_cred_dict, sheet_name='Lifts')
pb_df = get_google_sheet(sheet_url=sheet_url, credentials=google_sheet_cred_dict, sheet_name='PB')

# minor cleaning
lifts_df['Weight'] = lifts_df['Weight'].astype(float)
lifts_df['Reps'] = lifts_df['Reps'].astype(str)
lifts_df['Sets'] = lifts_df['Sets'].astype(int)
lifts_df['Notes'] = lifts_df['Notes'].astype(str)
lifts_df['Day'] = pd.to_datetime(lifts_df['Day'], format='%d/%m/%Y').dt.date

# add filter for exercise
# exercise_list_master = lifts_df['Exercise'].drop_duplicates()
# was sidebar input but now just normal
make_choice = st.selectbox('Select your Gym Exercise:', ['BENCH PRESS', 'SQUAT', 'DEADLIFT'])
#st.write('You selected:', make_choice)

# user date input
today = datetime.date.today()
tomorrow = today + datetime.timedelta(days=1)
start_date = st.date_input('Start date', (today - datetime.timedelta(days=60)))
end_date = st.date_input('End date', tomorrow)
if start_date < end_date:
    st.success('Start date: `%s`\n\nEnd date:`%s`' % (start_date, end_date))
else:
    st.error('Error: End date must fall after start date.')

# filter inputs
lifts_filt_df = lifts_df.loc[lifts_df["Exercise"] == make_choice]
lifts_filt_df = lifts_filt_df.loc[lifts_filt_df["Day"] >= start_date]
lifts_filt_df = lifts_filt_df.loc[lifts_filt_df["Day"] <= end_date]

# create and write graph
fig = px.line(lifts_filt_df, x="Day", y="Weight", color='Reps',markers=True, title=f'Powerlifting Performance: {make_choice}')
fig.update_traces(marker=dict(size=10))
st.write(fig)

# Looking at PBs
st.write('Gym PBs')
pb_df = lifts_df[lifts_df["Exercise"].isin(['BENCH PRESS', 'SQUAT', 'DEADLIFT'])]
pb_df['Weight'] = pb_df['Weight'].astype(float)
pb_df = pb_df.sort_values(by=['Exercise', 'Weight', 'Day'], ascending=[False, False,True]).drop_duplicates(['Exercise'])

# formatting for graph
pb_df['Reps'] = pb_df['Reps'].astype(str)
fig = px.bar(pb_df, x="Exercise", y="Weight", hover_data=['Day', 'Exercise', 'Weight', 'Reps'], color="Reps",
             barmode="group", title="All Time PB - Varying Reps ")
st.write(fig)