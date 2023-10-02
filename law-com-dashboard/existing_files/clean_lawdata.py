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

# Replace 'data.json' with the actual path to your JSON file
# with open(JSONFILE, 'r') as f:
#    data = json.load(f)


def load_json_file(filepath: Path) -> list[dict]:
    """
    Load the JSON file and return a list of dictionaries.
    """
    with open(filepath, "r") as f:
        data = json.load(f)
    return data


def sanitize_firm_data(data: list[dict]) -> list[dict]:
    """
    Sanitize the data by removing the entries that have corrupted revenue values or headcount values.
    """

    valid_firms = []

    for firm_data in data:
        revenue_values = firm_data.get("Revenue values")
        headcount_values = firm_data.get("Headcount values")
        if (
            revenue_values
            and headcount_values
            and len(revenue_values) == len(headcount_values) == len(range(1978, 2024))
        ):
            valid_firms.append(firm_data)

    return valid_firms


def convert_data_structure(data_list: list[dict]) -> dict:
    converted_data = {}

    for firm_data in data_list:
        # Extract the firm name and initialize dictionaries for revenue and headcount values
        firm_name = firm_data.pop("file")
        revenue_values = firm_data.pop("Revenue values")
        headcount_values = firm_data.pop("Headcount values")

        # Convert revenue_values and headcount_values lists to dictionaries with years as keys
        revenue_dict = {
            str(year): value for year, value in zip(range(1978, 2024), revenue_values)
        }
        headcount_dict = {
            str(year): value for year, value in zip(range(1978, 2024), headcount_values)
        }

        # Create a new dictionary with the desired structure
        new_data = {
            "Revenue values": revenue_dict,
            "Headcount values": headcount_dict,
        }

        # Update the converted_data dictionary with the new_data for the firm
        converted_data[firm_name] = new_data

    return converted_data


# Create a list of dictionaries with data for each year and each firm


def prepare_df_structure(converted_data):
    data_for_dataframe = []
    # Iterate through each firm and its corresponding data
    for firm, values in converted_data.items():
        revenue_values = values["Revenue values"]
        headcount_values = values["Headcount values"]

        # Create a dictionary for each year and firm with revenue and headcount values
        for year in range(1978, 2024):
            data_for_dataframe.append(
                {
                    "firm": firm,
                    "Year": year,
                    "Revenue": revenue_values.get(str(year), None),
                    "Headcount": headcount_values.get(str(year), None),
                }
            )
    return data_for_dataframe


# Print the resulting DataFrame
# print(df)

# num_unique_firms = df['firm'].nunique()


def create_ranked_table(df):
    # Sort the original DataFrame by revenues in descending order
    df_sorted_revenues = df.sort_values(by=["Year", "Revenue"], ascending=[True, False])

    # Create a new DataFrame 'revenues_df' to store the top 20 firms by revenue for each year
    revenues_df = pd.DataFrame()

    # Group the data by year
    grouped_revenues = df_sorted_revenues.groupby("Year")

    # Select the top 20 firms by revenue for each year and add them to the 'revenues_df'
    for year, group in grouped_revenues:
        top_20_revenues = group.head(20)
        revenues_df = revenues_df.append(top_20_revenues, ignore_index=True)

    # Sort the original DataFrame by headcount in descending order
    df_sorted_headcount = df.sort_values(
        by=["Year", "Headcount"], ascending=[True, False]
    )

    # Create a new DataFrame 'headcount_df' to store the top 20 firms by headcount for each year
    headcount_df = pd.DataFrame()

    # Group the data by year
    grouped_headcount = df_sorted_headcount.groupby("Year")

    # Select the top 20 firms by headcount for each year and add them to the 'headcount_df'
    for year, group in grouped_headcount:
        top_20_headcount = group.head(20)
        headcount_df = headcount_df.append(top_20_headcount, ignore_index=True)

    # Set the 'Year' column as the index for both DataFrames
    revenues_df.set_index("Year", inplace=True)
    headcount_df.set_index("Year", inplace=True)

    return revenues_df, headcount_df


# ranked_table = create_ranked_table(df)

# Print the resulting DataFrame
# print(ranked_table[0])
# print(ranked_table[1])


def last_20_years(df):
    # Consider only the last 20 years in the DataFrame
    df_last_20_years = df[df["Year"] >= 2004]

    # Sort the DataFrame by revenues and headcount in descending order
    df_sorted_revenues = df_last_20_years.sort_values(
        by=["Year", "Revenue"], ascending=[True, False]
    )
    df_sorted_headcount = df_last_20_years.sort_values(
        by=["Year", "Headcount"], ascending=[True, False]
    )

    # Create a new DataFrame 'revenues_df' to store the top 20 firms by revenue for each year
    revenues_df = pd.DataFrame()

    # Group the data by year
    grouped_revenues = df_sorted_revenues.groupby("Year")

    # Select the top 20 firms by revenue for each year and add them to the 'revenues_df'
    for year, group in grouped_revenues:
        top_20_revenues = group.head(20)
        revenues_df = revenues_df.append(top_20_revenues, ignore_index=True)

    # Create a new DataFrame 'headcount_df' to store the top 20 firms by headcount for each year
    headcount_df = pd.DataFrame()

    # Group the data by year
    grouped_headcount = df_sorted_headcount.groupby("Year")

    # Select the top 20 firms by headcount for each year and add them to the 'headcount_df'
    for year, group in grouped_headcount:
        top_20_headcount = group.head(20)
        headcount_df = headcount_df.append(top_20_headcount, ignore_index=True)

    # Set the 'Year' column as the index for both DataFrames
    revenues_df.set_index("Year", inplace=True)
    headcount_df.set_index("Year", inplace=True)

    # Print the resulting DataFrames with approximately 20 rows
    print("Revenues DataFrame (~20 rows):")
    print(revenues_df.head(20))
    print("\nHeadcount DataFrame (~20 rows):")
    print(headcount_df.head(20))


def visualize_changes(df):
    # Consider only the last 20 years in the DataFrame
    df_last_20_years = df[df["Year"] >= 2004]

    # Sort the DataFrame by revenues and headcount in descending order
    df_sorted_revenues = df_last_20_years.sort_values(
        by=["Year", "Revenue"], ascending=[True, False]
    )
    df_sorted_headcount = df_last_20_years.sort_values(
        by=["Year", "Headcount"], ascending=[True, False]
    )

    # Create a new DataFrame 'revenues_df' to store the top 20 firms by revenue for each year
    revenues_df = pd.DataFrame()

    # Group the data by year
    grouped_revenues = df_sorted_revenues.groupby("Year")

    # Select the top 20 firms by revenue for each year and add them to the 'revenues_df'
    for year, group in grouped_revenues:
        top_20_revenues = group.head(20)
        top_20_revenues = top_20_revenues[["firm", "Revenue"]]
        top_20_revenues.reset_index(drop=True, inplace=True)
        top_20_revenues.index += 1
        revenues_df = pd.concat(
            [revenues_df, top_20_revenues.rename(columns={"firm": f"{year} Revenue"})],
            axis=1,
        )

    # Create a new DataFrame 'headcount_df' to store the top 20 firms by headcount for each year
    headcount_df = pd.DataFrame()

    # Group the data by year
    grouped_headcount = df_sorted_headcount.groupby("Year")

    # Select the top 20 firms by headcount for each year and add them to the 'headcount_df'
    for year, group in grouped_headcount:
        top_20_headcount = group.head(20)
        top_20_headcount = top_20_headcount[["firm", "Headcount"]]
        top_20_headcount.reset_index(drop=True, inplace=True)
        top_20_headcount.index += 1
        headcount_df = pd.concat(
            [
                headcount_df,
                top_20_headcount.rename(columns={"firm": f"{year} Headcount"}),
            ],
            axis=1,
        )

    # Print the resulting DataFrames with the top 20 ranked firms by revenue and headcount for each year
    print("Revenues DataFrame (Top 20 ranked firms by revenue for each year):")
    print(revenues_df)
    print("\nHeadcount DataFrame (Top 20 ranked firms by headcount for each year):")
    print(headcount_df)

    return revenues_df, headcount_df


# visualize_changes(df)
# visualized_df_tuple = visualize_changes(df)


def output_excel(df_tuple):
    revenues_df = df_tuple[0]
    headcount_df = df_tuple[1]
    # Create an ExcelWriter object to write multiple DataFrames to the same Excel file
    with pd.ExcelWriter(OUTPUT_FILE_PATH, engine="xlsxwriter") as writer:
        # Write the 'revenues_df' DataFrame to the 'Revenues' sheet in the Excel file
        revenues_df.to_excel(writer, sheet_name="Revenues")

        # Write the 'headcount_df' DataFrame to the 'Headcount' sheet in the Excel file
        headcount_df.to_excel(writer, sheet_name="Headcount")

        # Get the xlsxwriter workbook and worksheet objects for further customization
        workbook = writer.book
        worksheet_revenues = writer.sheets["Revenues"]
        worksheet_headcount = writer.sheets["Headcount"]

        # Customize column widths
        for sheet, data_df in zip(
            [worksheet_revenues, worksheet_headcount], [revenues_df, headcount_df]
        ):
            for i, col in enumerate(data_df.columns):
                column_len = max(
                    data_df[col].astype(str).applymap(len).max(), len(col) + 2
                )
                sheet.set_column(i, i, column_len)

        # Add conditional formatting to highlight the top 20 firms in each year
        # You can customize the color and formatting as desired
        highlight_format = workbook.add_format({"bg_color": "#FFFF99", "bold": True})

        for sheet, data_df in zip(
            [worksheet_revenues, worksheet_headcount], [revenues_df, headcount_df]
        ):
            for i in range(1, len(data_df.columns) + 1):
                sheet.conditional_format(
                    1,
                    i,
                    21,
                    i,
                    {"type": "top", "value": 20, "format": highlight_format},
                )


# output_excel(visualized_df_tuple)


def save_to_sqlite(data_frame, db_file_name):
    """
    Save a DataFrame to an SQLite database.

    Parameters:
        data_frame (pd.DataFrame): The DataFrame to be saved.
        db_file_name (str): The name of the SQLite database file.

    Returns:
        None
    """
    try:
        # Connect to the SQLite database
        conn = sqlite3.connect(db_file_name)

        # Save the DataFrame to the database
        data_frame.to_sql("law_firm_data", conn, if_exists="replace", index=False)

        # Close the connection
        conn.close()

        print(f"Data saved to '{db_file_name}' database successfully.")
    except Exception as e:
        print(f"Error: {e}")


def visualize_changes_in_sqlite(db_file_name):
    # Connect to the SQLite database
    conn = sqlite3.connect(db_file_name)

    # Create temporary views for the required transformations
    create_view_revenues = """
        CREATE VIEW IF NOT EXISTS top_20_revenues AS
        SELECT Year, firm, Revenue
        FROM law_firm_data
        WHERE Year >= 2004
        ORDER BY Year ASC, Revenue DESC
        LIMIT 20;
    """

    create_view_headcount = """
        CREATE VIEW IF NOT EXISTS top_20_headcount AS
        SELECT Year, firm, Headcount
        FROM law_firm_data
        WHERE Year >= 2004
        ORDER BY Year ASC, Headcount DESC
        LIMIT 20;
    """

    # Execute the queries to create the views
    conn.execute(create_view_revenues)
    conn.execute(create_view_headcount)

    # Create the revenues DataFrame from the 'top_20_revenues' view
    revenues_df = pd.read_sql_query("SELECT * FROM top_20_revenues", conn).pivot(
        index="Year", columns="firm", values="Revenue"
    )

    # Create the headcount DataFrame from the 'top_20_headcount' view
    headcount_df = pd.read_sql_query("SELECT * FROM top_20_headcount", conn).pivot(
        index="Year", columns="firm", values="Headcount"
    )

    # Print the resulting DataFrames with the top 20 ranked firms by revenue and headcount for each year
    print("Revenues DataFrame (Top 20 ranked firms by revenue for each year):")
    print(revenues_df)
    print("\nHeadcount DataFrame (Top 20 ranked firms by headcount for each year):")
    print(headcount_df)

    # Close the connection
    conn.close()

    # return revenues_df, headcount_df


if __name__ == "__main__":
    data = load_json_file(JSONFILE)
    sanitized_data = sanitize_firm_data(data)
    converted_data = convert_data_structure(sanitized_data)
    data_for_dataframe = prepare_df_structure(converted_data)

    # Create a DataFrame from the list of dictionaries

    df = pd.DataFrame(data_for_dataframe)

    # output_file_path = 'output_file.xlsx'
    save_to_sqlite(df, "law_firm_database.db")
    visualize_changes_in_sqlite("law_firm_database.db")
    print("This script is being run directly.")
