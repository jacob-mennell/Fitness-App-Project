import pandas as pd
import datetime
import cherrypy
import fitbit
from gather_keys_oauth2 import OAuth2Server
import os

# sets the environment variables as python variables
CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')

# create a FitbitOauth2Client object.
server = OAuth2Server(CLIENT_ID, CLIENT_SECRET)
server.browser_authorize()
ACCESS_TOKEN = str(server.fitbit.client.session.token['access_token'])
REFRESH_TOKEN = str(server.fitbit.client.session.token['refresh_token'])
fitbit = fitbit.Fitbit(CLIENT_ID, CLIENT_SECRET, oauth2=True, access_token=ACCESS_TOKEN, refresh_token=REFRESH_TOKEN)

# define last 10 days of data
yesterday = str((datetime.datetime.now() - datetime.timedelta(days=1)).strftime("%Y%m%d"))
yesterday2 = str((datetime.datetime.now() - datetime.timedelta(days=2)).strftime("%Y-%m-%d"))
yesterday3 = str((datetime.datetime.now() - datetime.timedelta(days=3)).strftime("%Y-%m-%d"))
yesterday4 = str((datetime.datetime.now() - datetime.timedelta(days=4)).strftime("%Y-%m-%d"))
yesterday5 = str((datetime.datetime.now() - datetime.timedelta(days=5)).strftime("%Y-%m-%d"))
yesterday6 = str((datetime.datetime.now() - datetime.timedelta(days=6)).strftime("%Y-%m-%d"))
yesterday7 = str((datetime.datetime.now() - datetime.timedelta(days=7)).strftime("%Y-%m-%d"))
yesterday8 = str((datetime.datetime.now() - datetime.timedelta(days=8)).strftime("%Y-%m-%d"))
yesterday9 = str((datetime.datetime.now() - datetime.timedelta(days=9)).strftime("%Y-%m-%d"))
yesterday10 = str((datetime.datetime.now() - datetime.timedelta(days=10)).strftime("%Y-%m-%d"))
today = str(datetime.datetime.now().strftime("%Y%m%d"))

# variable list
id_list = []
name_list = []
calories_list = []
steps_list = []
date_list = []

days_list = [yesterday2, yesterday3, yesterday4, yesterday5, yesterday6, yesterday7, yesterday8, yesterday8, yesterday8]

# get activities for last 10 days
for day in days_list:
    activities = fitbit.activities(date=day)['activities']

    id_list_new = [action['activityId'] for action in activities]
    name_list_new = [action['name'] for action in activities]
    calories_list_new = [action['calories'] for action in activities]
    steps_list_new = [action['steps'] for action in activities]
    date_list_new = [action['startDate'] for action in activities]

    [id_list.append(x) for x in id_list_new]
    [name_list.append(x) for x in name_list_new]
    [calories_list.append(x) for x in calories_list_new]
    [steps_list.append(x) for x in steps_list_new]
    [date_list.append(x) for x in date_list_new]

# make DataFrame
activity_df = pd.DataFrame({'id': id_list,
                           'Name': name_list,
                           'Start Date': date_list,
                           'Calories': calories_list,
                           'Steps': steps_list
                           })

# return DataFrame
activity_df