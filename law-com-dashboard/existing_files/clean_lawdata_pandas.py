# clean_lawdata_pandas.py

import json
import sqlite3
from pathlib import Path

import pandas as pd

# Get the path of the current script
current_script_path = Path(__file__).resolve()

# Get the folder containing the current script
current_script_folder = current_script_path.parent

JSONFILE = Path(
    r"C:\Users\reubi\Coding\Projekte\Scrapelawcom\data\jsonfields\revenues_headcount.json"
)
OUTPUT_FILE_PATH = current_script_folder / r"output_file.xlsx"

if __name__ == "__main__":
    # Read the json file
    with open(JSONFILE, "r") as f:
        json_data = json.load(f)

    # Convert the json data to a pandas dataframe
    df = pd.DataFrame(json_data)
    df.rename(columns={"file": "Firm"}, inplace=True)

    # The sanitize firm function
    df = df[df["Revenue values"].apply(lambda x: len(x) == len(range(1978, 2024)))]
    df = df[df["Headcount values"].apply(lambda x: len(x) == len(range(1978, 2024)))]

    df.set_index("Firm", inplace=True)

    # Create a new DataFrame to store the transformed data
    df_transformed = pd.DataFrame()

    # Explode the "Revenue Values" and "Headcount Values" lists
    df_transformed["Revenue Values"] = df["Revenue values"].explode()
    df_transformed["Headcount Values"] = df["Headcount values"].explode()

    # Create the range [1978, 1979, 1980, ..., 2023]
    year_range = list(range(1978, 2024))

    # Repeat the range in every row of the "Year" column until all rows are full
    df_transformed["Year"] = (
        year_range * (len(df_transformed) // len(year_range))
        + year_range[: len(df_transformed) % len(year_range)]
    )

    # Reset the index "Firm" to a regular column

    df_transformed.reset_index(inplace=True)

    # Establish a connection to the SQLite database
    conn = sqlite3.connect("huge_firm_database.db")

    # Export the merged DataFrame to the SQL database
    df_transformed.to_sql("table_name", conn, if_exists="replace", index=False)

    # Close the database connection
    conn.close()
