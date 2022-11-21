# Fitness Project

Aims: 
- Record and visualise lift data from workouts
e.g. exercises, sets, reps and weight
- Use Google Sheets as a flexible data store to write gym session data via the gspread module
- Develop Streamlit web app (streamlit_app_gym.py) for user interface to input data to google cloud and to visualise lift trends.

Secondary: 
- Combine fitbit data with recorded data (Google Sheets) from workouts
e.g. exercises, sets, reps and weights (streamlit_app.py)
- Currently fitbit data is read from a _.pkl_ file due to issues accessing the data directly in the streamlit environment.

Link to reduced App with just Gym Data:
https://jacob-mennell-fitness-app-project-streamlit-app-gym-5dp6js.streamlit.app/

 pipreqs: 
- altair==4.1.0
- CherryPy==18.6.0
- fitbit==0.3.1
- gspread==5.6.2
- gspread_dataframe==3.3.0
- numpy==1.23.3
- oauthlib==3.2.2
- pandas==1.4.4
- plotly==5.9.0
- pytest==7.1.2
- streamlit==1.11.0

