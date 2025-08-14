import os
from concurrent.futures import ThreadPoolExecutor

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
        images_set = set().union(*mapping_dict.values())

        if self.use_threading:
            max_threads = min(64, len(images_set))
            with ThreadPoolExecutor(max_workers=max_threads) as executor:
                executor.map(self.download_with_scraper,images_set)
        else:
            for image in images_set:
                self.download_with_scraper(image)

        return WikipediaCollateralAdjectiveHTMLGenerator(
            output_dir=self.output_dir, output_file_name="output_file").generate_and_save(mapping_dict)

    def download_with_scraper(self, image_tuple):
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