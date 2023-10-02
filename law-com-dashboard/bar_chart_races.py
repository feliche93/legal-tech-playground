import os
import sqlite3
from pathlib import Path
import pandas as pd
import bar_chart_race as bcr  # type: ignore


def get_db_path():
    # Get the absolute path of the current script file
    script_location = Path(os.path.abspath(__file__)).resolve()

    # Get the parent directory of the script file
    parent_directory = script_location.parent

    # Construct the path to the database file
    db_path = parent_directory / "existing_files" / "law_firm_database.db"

    return db_path


def get_df(sql_query: str):
    db_path = get_db_path()

    conn = sqlite3.connect(str(db_path))

    df = pd.read_sql(con=conn, sql=sql_query)  # type: ignore

    return df


def create_bar_chart_race(df: pd.DataFrame, column: str, title: str):
    df_pivot = df.pivot(index="Year", columns="firm", values=column)

    bcr.bar_chart_race(  # type: ignore
        df=df_pivot,
        filename=f"{column}_bar_chart_race.mp4",
        title=title,
        orientation="h",
        sort="desc",
        n_bars=10,
        fixed_order=False,
        fixed_max=True,
        steps_per_period=200,
        period_length=2000,  # Increase this number to make the animation slower
        figsize=(6, 3.5),
    )


if __name__ == "__main__":
    # Get the data
    df_revenue = get_df("SELECT * FROM law_firm_data WHERE Revenue != 0")
    df_headcount = get_df("SELECT * FROM law_firm_data WHERE Headcount != 0")

    # Create the bar chart races
    create_bar_chart_race(df_revenue, "Revenue", "Law Firm Revenue Over Time")
    create_bar_chart_race(df_headcount, "Headcount", "Law Firm Headcount Over Time")
