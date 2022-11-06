import numpy as np
import altair as alt
import pandas as pd
import streamlit as st
import os
from google_sheets import get_google_sheet

st.header('test web app prior to loading fitness data')

# Example 1

st.write('Personal Fitness Data Application')

# Example 2

st.write('Gym History Table')

# Example 3

df = pd.DataFrame({
     'sessions': [1, 2, 3, 4],
     'weight': [10, 20, 30, 40]
     })

# make df from google sheets data
# sheet_url = os.getenv('sheet_url')
# df = get_google_sheet(sheet_url, 'PB')
# df = df.astype(str)
# test read in correctly
print(df.shape)

# st.write(df)
st.dataframe(df)


df2 = pd.DataFrame(
     np.random.randn(200, 3),
     columns=['a', 'b', 'c'])

c = alt.Chart(df2).mark_circle().encode(
     x='a', y='b', size='c', color='c', tooltip=['a', 'b', 'c'])

st.write(c)