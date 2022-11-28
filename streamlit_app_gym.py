import numpy as np
import altair as alt
import pandas as pd
import streamlit as st
import os
from get_google_sheets_data import get_google_sheet, export_to_google_sheets
import datetime
import plotly.express as px
import plotly.figure_factory as ff

######################## Streamlit Specific  Functions ########################

def add_dfForm():
    """ Sets keys to add pd dataframe to session state data"""
    row = pd.DataFrame({'Day': [st.session_state.input_date],
                        'Exercise': [st.session_state.input_exercise],
                        'Weight': [st.session_state.input_weight],
                        'Reps': [st.session_state.input_reps],
                        'Sets': [st.session_state.input_sets],
                        'Notes': [st.session_state.input_notes],
                        'User': [st.session_state.input_name]
                        })
    st.session_state.data = pd.concat([st.session_state.data, row])


def check_password():
    """Returns `True` if the user had the correct password."""

    def password_entered():
        """Checks whether a password entered by the user is correct."""
        if st.session_state["password"] == st.secrets["PASSWORD"]:
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # don't store password
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        # First run, show input for password.
        st.text_input(
            "Need Password to input data", type="password", on_change=password_entered, key="password"
        )
        return False
    elif not st.session_state["password_correct"]:
        # Password not correct, show input + error.
        st.text_input(
            "Need Password to input data", type="password", on_change=password_entered, key="password"
        )
        st.error("😕 Password incorrect")
        return False
    else:
        # Password correct.
        return True


############################## streamlit app #############################

# using st.secrets
sheet_url = st.secrets['SHEET_URL']
google_sheet_cred_dict = st.secrets['GOOGLE_SHEET_CRED']

# set streamlit app headers
st.header('Fitness Monitoring App')
st.write('App allows user input of gym performance and visualisation of historic performance.')

# input new data
st.subheader('Record Sets')

if check_password():

    if 'data' not in st.session_state:
        data = pd.DataFrame({'Day': [],
                             'Exercise': [],
                             'Weight': [],
                             'Reps': [],
                             'Sets': [],
                             'Notes': [],
                             'User': []})
        st.session_state.data = data

    data = st.session_state.data

    dfForm = st.form(key='dfForm')
    with dfForm:
        dfColumns = st.columns(7)
        with dfColumns[0]:
            st.date_input('Day', key='input_date')
        with dfColumns[1]:
            st.selectbox('Exercise', ['BENCH PRESS', 'SQUAT', 'DEADLIFT'], key='input_exercise')
        with dfColumns[2]:
            st.number_input('Weight', key='input_weight', min_value=1, max_value=200, value=100, step=1)
        with dfColumns[3]:
            st.number_input('Reps', key='input_reps', min_value=1, max_value=20, value=8, step=1)
        with dfColumns[4]:
            st.number_input('Sets', key='input_sets', min_value=1, max_value=5, value=3, step=1)
        with dfColumns[5]:
            st.text_input('Notes', key='input_notes')
        with dfColumns[6]:
            st.text_input('User', key='input_name', value='JM')

        st.form_submit_button(on_click=add_dfForm)

    # send data back to Google Sheets for storage
    export_to_google_sheets(sheet_url=sheet_url, df_new=data, credentials=google_sheet_cred_dict, sheet_name='Lifts')

################### historical lifts from google sheets ##################
# data soon to read directly from SQL

# set headers
st.subheader('Performance Tracking')

# get data using gspread
lifts_df = get_google_sheet(sheet_url=sheet_url, credentials=google_sheet_cred_dict, sheet_name='Lifts')

# minor cleaning
lifts_df['Weight'] = lifts_df['Weight'].astype(float)
lifts_df['Reps'] = lifts_df['Reps'].astype(str)
lifts_df['Sets'] = lifts_df['Sets'].astype(int)
lifts_df['Notes'] = lifts_df['Notes'].astype(str)
lifts_df['Day'] = pd.to_datetime(lifts_df['Day'], format='%d/%m/%Y').dt.date

# add filter for exercise

### code for auto excerse list ###
# exercise_list_master = lifts_df['Exercise'].drop_duplicates()

# manual input for now as just 3 exercises
make_choice = st.selectbox('Select your Gym Exercise:', ['BENCH PRESS', 'SQUAT', 'DEADLIFT'])

# user data input
user_list = lifts_df['User'].drop_duplicates().to_list()
user_choice = st.selectbox('Select lifter:', user_list)

###  code for streamlit date slider ###
# today_date = datetime.date.today()
# previous_date = today_date - datetime.timedelta(days=60)
# date_format = 'MMM DD, YYYY'
# prev_slider = st.slider('Select min date', min_value=previous_date, value=previous_date, max_value=today_date, format=date_format)

### code for manual date input ###
# start_date = st.date_input('Start date', (today - datetime.timedelta(days=60)))
# end_date = st.date_input('End date', tomorrow)
# if start_date < end_date:
#     st.success('Start date: `%s`\n\nEnd date:`%s`' % (start_date, end_date))
# else:
#     st.error('Error: End date must fall after start date.')

# filter inputs
lifts_filt_df = lifts_df.loc[lifts_df["User"] == user_choice]
lifts_filt_df = lifts_filt_df.loc[lifts_filt_df["Exercise"] == make_choice]

### code for date filter using plotly filter for now ###
# lifts_filt_df = lifts_filt_df.loc[lifts_filt_df["Day"] >= prev_slider]
# lifts_filt_df = lifts_filt_df.loc[lifts_filt_df["Day"] <= today_date]

# create and write graph
fig = px.line(lifts_filt_df, x="Day", y="Weight", color='Reps', markers=True,
              title=f'Powerlifting Performance: {make_choice}')
fig.update_traces(marker=dict(size=10))

# Add range slider to plotly figure
fig.update_layout(
    xaxis=dict(
        rangeselector=dict(
            buttons=list([
                dict(count=7,
                     label="7d",
                     step="day",
                     stepmode="backward"),
                dict(count=14,
                     label="14d",
                     step="day",
                     stepmode="backward"),
                dict(count=1,
                     label="1m",
                     step="month",
                     stepmode="backward"),
                dict(count=2,
                     label="2m",
                     step="month",
                     stepmode="backward"),
                dict(step="all")
            ])
        ),
        rangeslider=dict(
            visible=True),
        type="date"
    ),
    template='plotly_dark',
    xaxis_rangeselector_font_color='black',
    xaxis_rangeselector_font_size=16,
    xaxis_rangeselector_activecolor='red',
    xaxis_rangeselector_bgcolor='green')

st.plotly_chart(fig, use_container_width=True)

# Looking at PBs
# set headers
st.subheader('User PB Comparison')
pb_df = lifts_df[lifts_df["Exercise"].isin(['BENCH PRESS', 'SQUAT', 'DEADLIFT'])]
pb_df['Weight'] = pb_df['Weight'].astype(float)
pb_df = pb_df.sort_values(by=['User', 'Exercise', 'Weight', 'Day'],
                          ascending=[False, False, False, True]).drop_duplicates(['User', 'Exercise'])

# graph formatting
pb_df['Reps'] = pb_df['Reps'].astype(str)
fig = px.bar(pb_df,
             x="Exercise",
             y="Weight",
             hover_data=['Day', 'Exercise', 'Weight', 'Reps'],
             color="User",
             barmode="group",
             title="All Time PB - Varying Reps ")
st.plotly_chart(fig, use_container_width=True)
