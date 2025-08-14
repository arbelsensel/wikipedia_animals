import os
import webbrowser
import logging

from scrapers.wikipedia_collateral_adjective_scraper import WikipediaCollateralAdjectiveScraper

logging.basicConfig(
    level=logging.INFO,
)

WIKI_URL = "https://en.wikipedia.org/wiki/List_of_animal_names"
LOCAL_TMP_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "tmp")

if __name__ == "__main__":
    scraper = WikipediaCollateralAdjectiveScraper(url=WIKI_URL, threading=True, output_dir=LOCAL_TMP_DIR)

    output_file_path = scraper.scrape()

    webbrowser.open_new_tab(output_file_path)
