import os
from concurrent.futures import ThreadPoolExecutor
from typing import Set, Tuple

from components.fetchers.image_downloader import ImageDownloader
from components.html_generator.wikipedia_html_generators import WikipediaCollateralAdjectiveHTMLGenerator
from components.scrapers.base_scrapers import TableMappingScraper
from components.scrapers.wikipedia_scraper import WikiScraper
from components.scrapers.extractors.wikipedia_extractors import CollateralAdjectivesExtractor, AnimalExtractor


class WikipediaCollateralAdjectiveScraper(WikiScraper):
    """
    Scraper for collateral adjectives of animals out of wikipedia page.
    It manages the scraping process and all the relevant components.
    Also holding the relevant args as class properties (KEY_HEADER, VALUE_HEADER, WIKI_URL)
    """

    WIKI_URL = "https://en.wikipedia.org/wiki/List_of_animal_names"
    KEY_HEADER = "Collateral adjective"
    VALUE_HEADER = "Animal"
    MAX_THREADS = 64

    def __init__(self, output_dir: str, use_threading: bool = True):
        """
        WikipediaCollateralAdjectiveScraper constructor
        :param output_dir: Directory to save output to
        """
        super().__init__(url=self.WIKI_URL)
        self.output_dir = output_dir
        self.use_threading = use_threading

        self.create_output_dir()

    def scrape(self):
        """
        Scrapes wikipedia page to get collateral adjectives mapped to animals list
        """
        table, key_idx, value_idx = self.get_table_to_map(self.KEY_HEADER, self.VALUE_HEADER)

        table_scraper = TableMappingScraper(table=table,
                                            keys_extractor=CollateralAdjectivesExtractor(col_idx=key_idx),
                                            values_extractor=AnimalExtractor(col_idx=value_idx))

        mapping_dict = table_scraper.create_mapping()

        # creating set of tuples (animal_name, animal_page_url) to avoid collisions
        # of same image treated more than once
        images_set = set().union(*mapping_dict.values())
        self.download_images_with_scraper(images_set)

        return WikipediaCollateralAdjectiveHTMLGenerator(
            output_dir=self.output_dir, output_file_name="output_file").generate_and_save(mapping_dict)

    def download_images_with_scraper(self, images_set: Set[Tuple[str, str]]):
        """
        Method to handle get images requests and download them
        If use_threading is True will use ThreadPoolExecutor, otherwise will loop over them.
        :param images_set:
        """

        ### The download_image_with_scraper is mostly I/O bound task since it's getting the image by request
        ### and then writing it to disk, therefore its make sense to use multithreading over it.

        if self.use_threading:
            max_threads = min(self.MAX_THREADS, len(images_set))
            with ThreadPoolExecutor(max_workers=max_threads) as executor:
                executor.map(self.download_image_with_scraper,images_set)
        else:
            for image in images_set:
                self.download_image_with_scraper(image)

    def download_image_with_scraper(self, image_tuple):
        """
        Scrapes wikipedia page to get image url and download it
        :param image_tuple: tuple of (image_name, page_url)
        """
        image_name, page_url = image_tuple
        image_url = WikiScraper(url=page_url).get_image_url()
        if image_url:
            ImageDownloader(file_name=image_name, url=image_url, directory=self.output_dir).download()
        else:
            self.logger.warning(f"No image found for {image_name} at {page_url}")

    def create_output_dir(self):
        """
        Creates output directory, if it doesn't exist
        """
        os.makedirs(self.output_dir, exist_ok=True)
        self.logger.info(f"Created output directory {self.output_dir}")