import os
from concurrent.futures import ThreadPoolExecutor

from fetchers.image_downloader import ImageDownloader
from output_handler import generate_html
from scrapers.base_scrapers import TableMappingScraper
from scrapers.wikipedia_scraper import WikiScraper
from scrapers.extractors.wikipedia_extractors import CollateralAdjectivesExtractor, AnimalExtractor


class WikipediaCollateralAdjectiveScraper(WikiScraper):
    KEY_HEADER = "Collateral adjective"
    VALUE_HEADER = "Animal"

    def __init__(self, output_dir: str, threading: bool = True, *args, **kwargs):
        """
        WikipediaCollateralAdjectiveScraper constructor
        :param output_dir: Directory to save output to
        :param args:
        :param kwargs:
        """
        super().__init__(*args, **kwargs)
        self.output_dir = output_dir
        self.threading = threading

        self.create_output_dir()

    def scrape(self):
        """
        scrapes wikipedia page to get collateral adjectives mapped to animals list
        """
        table, key_idx, value_idx = self.get_table_to_map(self.KEY_HEADER, self.VALUE_HEADER)

        table_scraper = TableMappingScraper(table=table,
                                            keys_extractor=CollateralAdjectivesExtractor(col_idx=key_idx),
                                            values_extractor=AnimalExtractor(col_idx=value_idx))

        mapping_dict = table_scraper.create_mapping()
        images_set = set().union(*mapping_dict.values())


        if self.threading:
            max_threads = min(32, len(images_set))
            with ThreadPoolExecutor(max_workers=max_threads) as executor:
                executor.map(self.download_with_scraper,images_set)
        else:
            for image in images_set:
                self.download_with_scraper(image)

        output_file_path = generate_html(mapping=mapping_dict,
                                  tmp_dir=self.output_dir)

        self.logger.info(f"output file saved to {output_file_path}")

        return output_file_path

    def download_with_scraper(self, image_tuple):
        image_name, page_url = image_tuple
        image_url = WikiScraper(url=page_url).get_image_url()
        if image_url:
            ImageDownloader(file_name=image_name, url=image_url, directory=self.output_dir).download()
        else:
            self.logger.warning(f"No image found for {image_name} at {page_url}")

    def create_output_dir(self):
        os.makedirs(self.output_dir, exist_ok=True)
        self.logger.info(f"Created output directory {self.output_dir}")