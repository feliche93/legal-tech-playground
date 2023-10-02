import json
import time
from pathlib import Path

from bs4 import BeautifulSoup
from tqdm import tqdm  # Import tqdm for the progress bar

OUTPUT_DIR = Path(r"C:\Users\reubi\Coding\Projekte\Scrapelawcom\data\jsonfields")
INPUT_DIR = Path(r"C:\Users\reubi\Coding\Projekte\Scrapelawcom\data\html")


# Custom decorator to measure the time taken for a function
def timing_decorator(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"Time taken for {func.__name__}: {end_time - start_time:.2f}s")
        return result

    return wrapper


@timing_decorator
def scrape_overview(html_file: str) -> dict:
    target_file = INPUT_DIR / html_file

    with open(target_file, "r", encoding="utf-8") as file:
        html_content = file.read()

        soup = BeautifulSoup(html_content, "html.parser")

    # Find the overview section
    overview_section = soup.find(
        "h4", class_="section-title-firms", string="Overview"
    ).find_next("ul", class_="overview")

    # Extract the values of the specified fields
    fields = [
        "Global Rank:",
        "Total Offices:",
        "Total Headcount*:",
        "Equity Partners:",
        "Non-Equity Partners:",
        "Associates:",
        "Total Revenue:",
        "Profit Per Equity Partner:",
        "Revenue Per Lawyer:",
    ]
    data = {}

    for field in fields:
        label = overview_section.find("p", class_="overview-title", string=field)
        if label:
            value = label.find_next("div").get_text(strip=True)
            data[field] = value

    return data


def get_html_files_in_folder(folder_path) -> list:
    folder_path = Path(folder_path)
    html_files = [file for file in folder_path.glob("*.html") if file.is_file()]
    return html_files


if __name__ == "__main__":
    # Das ist einfach eine LIste der html files
    OUTPUT_FILE = OUTPUT_DIR / "example_data.json"

    html_files = get_html_files_in_folder(INPUT_DIR)

    placeholder = []

    for file in tqdm(html_files, desc="Scraping overview data", unit="file"):
        try:
            data = scrape_overview(file)
            file_name_without_extension = Path(file).stem
            data["file"] = file_name_without_extension
            placeholder.append(data)
        except:
            continue

    with open(OUTPUT_FILE, "w", encoding="utf-8") as json_file:
        json.dump(placeholder, json_file, ensure_ascii=False, indent=4)
