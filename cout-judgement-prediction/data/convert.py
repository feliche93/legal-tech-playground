from pathlib import Path

import pandas as pd


def read_json_to_dataframe():
    eug_applications_path = Path('./eug_applications.json')

    eug_applications_df = pd.read_json(eug_applications_path)

    # Keep only the 'Case' and 'Date' columns from eug_applications_df
    eug_applications_df = eug_applications_df[['Case', 'Date']]

    # Rename 'Date' column to 'Application Date'
    eug_applications_df.rename(columns={'Date': 'Application Date'}, inplace=True)

    eug_judgments_path = Path('./eug_judgments.json')

    eug_judgments_df = pd.read_json(eug_judgments_path)

    eug_judgments_df.rename(columns={'Date': 'Judgment Date'}, inplace=True)

    # Perform a left join on 'Case'
    merged_df = pd.merge(eug_judgments_df, eug_applications_df, on='Case', how='left')

    # convert column names to snake case

    merged_df.columns = (
        merged_df.columns.str.lower()
        .str.replace(' ', '_')
        .str.replace('(', '')
        .str.replace(')', '')
        .str.replace('-', '_')
    )

    # calculate the difference between the application date and the judgment date in days
    merged_df['days_to_judgment'] = (
        merged_df['judgment_date'] - merged_df['application_date']
    ).dt.days

    # drop na for days_to_judgment
    merged_df.dropna(subset=['days_to_judgment'], inplace=True)

    return merged_df


merged_df = read_json_to_dataframe()

merged_df.to_csv('eug_judgments_raw.csv', index=False)
