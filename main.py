import os
import logging
import webbrowser
from concurrent.futures import ThreadPoolExecutor
import urllib.parse as urlparse

from output_handler import generate_html
from scrapers.base_scrapers import TableMappingScraper, BaseHTMLScraper
from scrapers.wikipedia_structures import WikiScraper, CollateralAdjectivesExtractor, AnimalExtractor

URL_PREFIX = "https://en.wikipedia.org"
LIST_OF_ANIMAL_URL = "/wiki/List_of_animal_names"
TABLE_HEADERS = ['Collateral adjective', 'Animal']

WIKI_URL = urlparse.urljoin(URL_PREFIX, LIST_OF_ANIMAL_URL)
LOCAL_TMP_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "tmp")

def download_image(url: str, image_name: str, directory: str=LOCAL_TMP_DIR):
    try:
        WikiScraper(url).download_image(image_name=image_name, directory=directory)
    except Exception as e:
        logging.error(f"Error downloading image {image_name}: {e}", exc_info=True)

if __name__ == "__main__":
    scraper = BaseHTMLScraper(url=WIKI_URL)
    table, key_idx, value_idx = scraper.get_table_to_map(*TABLE_HEADERS)
    collateral_adjective_extractor = CollateralAdjectivesExtractor(col_idx=key_idx)
    animal_extractor = AnimalExtractor(col_idx=value_idx)

    table_scraper = TableMappingScraper(table, collateral_adjective_extractor, animal_extractor)
    mapping_dict = table_scraper.create_mapping()

    images_dict = {}
    for adj, animals_list in mapping_dict.items():
        for d in animals_list:
            images_dict[d['name']] = urlparse.urljoin(URL_PREFIX, d['href'])

    os.makedirs("tmp", exist_ok=True)

    max_threads = min(32, len(images_dict))
    with ThreadPoolExecutor(max_workers=max_threads) as executor:
        executor.map(lambda args: download_image(*args), zip(images_dict.values(), images_dict.keys()))

    file_path = generate_html(mapping=mapping_dict, tmp_dir=os.path.join(os.path.dirname(os.path.abspath(__file__)), "tmp"))
    logging.info(f"output file saved to {file_path}")
    webbrowser.open(os.path.abspath(file_path))
    logging.info("Done")
