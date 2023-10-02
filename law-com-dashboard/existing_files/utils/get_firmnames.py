import json
import re
from pathlib import Path

from bs4 import BeautifulSoup

HTML_FILE = Path(
    r"C:\Users\reubi\Coding\Projekte\Scrapelawcom\data\Coverage & Rankings of Top Law Firms.html"
)

OUTPUT_FOLDER = Path(r"C:\Users\reubi\Coding\Projekte\Scrapelawcom\data")
OUTPUT_FILE = OUTPUT_FOLDER / "firmnames.json"

with open(HTML_FILE, "r", encoding="utf-8") as file:
    html_content = file.read()

soup = BeautifulSoup(html_content, "html.parser")

ul_element = soup.find("ul", class_="article-list-default firm-list")
h4_elements = ul_element.find_all("h4", class_="article-title")

links_and_texts = []
for h4_element in h4_elements:
    link = h4_element.find("a")["href"]
    text = h4_element.find("a").text
    links_and_texts.append((link, text))

# Print the result
for link, text in links_and_texts:
    print(f"Link: {link}, Text: {text}")


def sanitize_windows_filename(filename):
    # Characters that are not allowed in Windows file names
    invalid_chars = r'[<>:"/\\|?*]'

    # Replace invalid characters with underscores
    sanitized_filename = re.sub(invalid_chars, "_", filename)

    # Remove all whitespace and "&" characters
    sanitized_filename = sanitized_filename.replace(" ", "").replace("&", "")

    # Remove leading/trailing dots
    sanitized_filename = sanitized_filename.strip(".")

    # Limit the file name to a reasonable length (max 255 characters in Windows)
    max_filename_length = 255
    sanitized_filename = sanitized_filename[:max_filename_length]

    return sanitized_filename


# Convert the list of tuples to a list of dictionaries
converted_data = [
    {"link": link, "firm": firm, "filestem": sanitize_windows_filename(firm)}
    for link, firm in links_and_texts
]

# Save the data to a .json file
with open(OUTPUT_FILE, "w", encoding="utf-8") as json_file:
    json.dump(converted_data, json_file, ensure_ascii=False, indent=4)

print("Data saved to 'output.json' successfully.")
