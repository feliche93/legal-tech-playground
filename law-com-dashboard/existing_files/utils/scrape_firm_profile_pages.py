import json
import time
from pathlib import Path

from playwright.sync_api import sync_playwright

JSON_INPUT = Path(r"C:\Users\reubi\Coding\Projekte\Scrapelawcom\data\firmnames_p2.json")


def save_homepage_response(url, output_file):
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()

        # Start the timer
        start_time = time.time()

        page.goto(url)

        # Wait for any necessary elements to load (if needed)
        # You can use page.wait_for_selector or other similar methods here

        # Get the page content
        content = page.content()

        # Save the content to a file
        with open(output_file, "w", encoding="utf-8") as file:
            file.write(content)

        browser.close()

        # Calculate and print the elapsed time
        end_time = time.time()
        elapsed_time = end_time - start_time
        print(f"Time taken: {elapsed_time:.2f} seconds")


def load_json_file(filename=JSON_INPUT):
    with open(filename, "r", encoding="utf-8") as file:
        data = json.load(file)
    return data


def convert_filestem(filestem: str) -> Path:
    filename = f"{filestem}.html"
    output_file = OUTPUT_DIR / filename
    return output_file


if __name__ == "__main__":
    # Replace 'https://example.com' with the homepage URL you want to open
    # url = 'https://www.law.com/law-firm-profile/?id=173&name=Kirkland-%26-Ellis-LLP/'

    # Replace 'output.html' with the desired output file path and name
    # output_file = 'output.html'

    data = load_json_file()

    for entry in data:
        save_homepage_response(entry["link"], convert_filestem(entry["filestem"]))
        time.sleep(10)
