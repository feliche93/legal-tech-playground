import pandas as pd
from pathlib import Path
import json 

JSONFILE = Path(r"C:\Users\reubi\Coding\Projekte\Scrapelawcom\data\jsonfields\revenues_headcount.json")


# Replace 'data.json' with the actual path to your JSON file
with open(JSONFILE, 'r') as f:
    data = json.load(f)

valid_firms = []

# Check for corrupted entries and filter them out
for firm_data in data:
    revenue_values = firm_data.get("Revenue values")
    headcount_values = firm_data.get("Headcount values")
    if revenue_values and headcount_values and len(revenue_values) == len(headcount_values) == len(range(1978, 2024)):
        valid_firms.append(firm_data)

# Convert the valid firm data to a pandas DataFrame
df = pd.DataFrame(valid_firms)

# If you want to set the 'file' column as the DataFrame index, you can use:
df.set_index('file', inplace=True)

# Print the resulting DataFrame
#print(df)

def growth_rate(start_year, end_year):
    # Calculate the growth rate for each firm between the specified years
    df['Revenue Growth'] = (df['Revenue values'].apply(lambda x: x[end_year - 1978]) -
                            df['Revenue values'].apply(lambda x: x[start_year - 1978])) / df['Revenue values'].apply(lambda x: x[start_year - 1978])

    df['Headcount Growth'] = (df['Headcount values'].apply(lambda x: x[end_year - 1978]) -
                              df['Headcount values'].apply(lambda x: x[start_year - 1978])) / df['Headcount values'].apply(lambda x: x[start_year - 1978])

    # Return the DataFrame with the calculated growth rates
    return df

# Call the function with desired start and end years (e.g., from 2010 to 2023)
result_df = growth_rate(2015, 2023)

# Print the resulting DataFrame with growth rates
print(result_df)

output_file_path = 'output_file.xlsx'
result_df.to_excel(output_file_path)  # Set index=False to exclude the index from the exported Excel file
