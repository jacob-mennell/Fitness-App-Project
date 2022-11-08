import pandas as pd
import datetime
import cherrypy
import fitbit
from gather_keys_oauth2 import OAuth2Server
import os
import json

class FitbitAnalysis:

    def __init__(self, client_id: str, client_secret: str):
        self.client_id = client_id
        self.client_secret = client_secret

        # create a FitbitOauth2Client object.
        server = OAuth2Server(self.client_id,self.client_secret)
        server.browser_authorize()
        ACCESS_TOKEN = str(server.fitbit.client.session.token['access_token'])
        REFRESH_TOKEN = str(server.fitbit.client.session.token['refresh_token'])

        self.fit = fitbit.Fitbit(client_id, client_secret, oauth2=True, access_token=ACCESS_TOKEN,
                            refresh_token=REFRESH_TOKEN)


    def get_x_days_activity(self, no_days_ago: int) -> pd.DataFrame:

        # define last 10 days of data
        days_list = []
        for i in range(1, no_days_ago+1):
            days_list.append(str((datetime.datetime.now() - datetime.timedelta(days=i)).strftime("%Y-%m-%d")))

        # variable list
        id_list = []
        name_list = []
        calories_list = []
        steps_list = []
        date_list = []

        # get activities for last x days
        for day in days_list:
            activities = self.fit.activities(date=day)['activities']
            [id_list.append(x) for x in [action['activityId'] for action in activities]]
            [name_list.append(x) for x in [action['name'] for action in activities]]
            [calories_list.append(x) for x in [action['calories'] for action in activities]]
            [steps_list.append(x) for x in [action['steps'] for action in activities]]
            [date_list.append(x) for x in [action['startDate'] for action in activities]]

        # make DataFrame
        activity_df = pd.DataFrame({'id': id_list,
                                   'Name': name_list,
                                   'Start_Date': date_list,
                                   'Calories': calories_list,
                                   'Steps': steps_list
                                   })

        # cast data types
        activity_df['id'] = activity_df['id'].astype(int)
        activity_df['Name'] = activity_df['Name'].astype(str)
        activity_df['Start_Date'] = pd.to_datetime(activity_df['Start_Date'], format='%Y-%m-%d')
        activity_df['Steps'] = activity_df['Steps'].astype(int)
        activity_df['Calories'] = activity_df['Calories'].astype(int)

        # return DataFrame
        return activity_df


    def get_x_days_sleep(self, no_days_ago: int) -> pd.DataFrame:

        # define last 10 days of data
        days_list = []
        for i in range(1, no_days_ago + 1):
            days_list.append(str((datetime.datetime.now() - datetime.timedelta(days=i)).strftime("%Y-%m-%d")))

        # get activities for last x days
        sleep_time_list = []
        sleep_val_list = []
        for day in days_list:
            sleep_func = self.fit.sleep(date=day)
            for i in sleep_func['sleep'][0]['minuteData']:
                sleep_time_list.append(i['dateTime'])
                sleep_val_list.append(i['value'])

        sleep_df = pd.DataFrame({'State': sleep_val_list,
                                 'Time': sleep_time_list})

        return sleep_df

# get credentials for api and google sheet source
with open('cred.json') as data_file:
    data = json.load(data_file)

# export fitbit data to pkl file
fitinst = FitbitAnalysis(data['client_id'], data['client_secret'])
activity = fitinst.get_x_days_activity(30)
activity.to_pickle('activity.pkl')

sleep = fitinst.get_x_days_sleep(30)
sleep.to_pickle('sleep.pkl')
