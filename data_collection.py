import pandas as pd
import datetime
import cherrypy
import fitbit
from gather_keys_oauth2 import OAuth2Server
import os

# set the environment variables as python variables
CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')

# create a FitbitOauth2Client object.
server = OAuth2Server(CLIENT_ID, CLIENT_SECRET)
server.browser_authorize()
ACCESS_TOKEN = str(server.fitbit.client.session.token['access_token'])
REFRESH_TOKEN = str(server.fitbit.client.session.token['refresh_token'])
fitbit = fitbit.Fitbit(CLIENT_ID, CLIENT_SECRET, oauth2=True, access_token=ACCESS_TOKEN, refresh_token=REFRESH_TOKEN)

# define last 10 days of data
days_list = []
for i in range(1, 11):
    days_list.append(str((datetime.datetime.now() - datetime.timedelta(days=i)).strftime("%Y-%m-%d")))

# variable list
id_list = []
name_list = []
calories_list = []
steps_list = []
date_list = []

# get activities for last 10 days
for day in days_list:
    activities = fitbit.activities(date=day)['activities']
    [id_list.append(x) for x in [action['activityId'] for action in activities]]
    [name_list.append(x) for x in [action['name'] for action in activities]]
    [calories_list.append(x) for x in [action['calories'] for action in activities]]
    [steps_list.append(x) for x in [action['steps'] for action in activities]]
    [date_list.append(x) for x in [action['startDate'] for action in activities]]

# make DataFrame
activity_df = pd.DataFrame({'id': id_list,
                           'Name': name_list,
                           'Start Date': date_list,
                           'Calories': calories_list,
                           'Steps': steps_list
                           })

# return DataFrame
activity_df