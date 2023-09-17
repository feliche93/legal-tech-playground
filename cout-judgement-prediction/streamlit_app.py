from pathlib import Path

import pandas as pd
import streamlit as st

"""
# Court Judgement Prediction 🤖

Predicting the court date of a case based on the case details.
"""

cwd = Path.cwd()

st.write(cwd)

file_path = cwd / 'data' / 'Search results 20230821.csv'

df = pd.read_csv(file_path.as_posix(), on_bad_lines="warn")


st.write(df.columns)

st.write(df.head())
