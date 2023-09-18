import pathlib

import pandas as pd
import streamlit as st
from pycaret.regression import RegressionExperiment

s = RegressionExperiment()

cwd = pathlib.Path.cwd()

file_path = cwd / 'cout-judgement-prediction' / 'data' / 'eug_judgments_raw.csv'

df = pd.read_csv(
    file_path.as_posix(),
    # on_bad_lines="warn"
)

subject_matter_options = df['subject_matter'].unique().tolist()

st.title('Judgement Prediction')

st.write('This is a web app to predict the number of days to judgement.')

st.text('Please enter the following information:')


subject_matter = st.selectbox('Subject matter', subject_matter_options)

application_date = st.date_input('Application date')

predict_df = pd.DataFrame(
    {
        'subject_matter': subject_matter,
        'application_date': application_date,
    },
    index=[0],
)

predict_df['application_date'] = pd.to_datetime(predict_df['application_date'])

model_file_path = cwd / 'cout-judgement-prediction' / 'ml' / 'best_pipeline'

final_best = s.load_model(model_file_path.as_posix())

prediction = s.predict_model(final_best, predict_df)

days = prediction['prediction_label'].values[0].round(1)

st.subheader('Prediction')

if days:
    st.write(f'The number of days to judgement is {days} days.')
