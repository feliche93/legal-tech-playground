import pandas as pd
import pathlib

cwd = pathlib.Path.cwd()

file_path = cwd.parent / 'data' / 'Search results 20230821.csv'

df = pd.read_csv(file_path.as_posix(), 
                 #on_bad_lines="warn"
                 )

target_columns = [

    "Date of document",
    "Date lodged",
    "Type of procedure",
    "Applicant/Appellant",
    "Defendant/Other parties to the proceedings",
    "Judge-Rapporteur",
    "Country or organisation from which the request originates",
]

df = df[target_columns]

with open(file_path.as_posix(), 'r') as file:
    lines = file.readlines()
    problematic_lines = [806, 897, 904]  # ... add other line numbers
    for line_num in problematic_lines:
        print(f"Line {line_num}: {lines[line_num-1]}")  # -1 because list indexing starts from 0
