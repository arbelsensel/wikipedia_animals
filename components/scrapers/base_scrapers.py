import logging
from collections import defaultdict
from typing import Tuple, List, Dict

from bs4 import BeautifulSoup, Tag, ResultSet

from components.scrapers.extractors.base_extractor import BaseCellsExtractor
from components.fetchers.base_fetcher import BaseHTMLFetcher
from components.fetchers.image_downloader import ImageDownloader


class ImageNotFound(Exception):
    pass


class BaseHTMLScraper:
    """
    Base class for fetchers page scrapers
    """
    def __init__(self, url: str, *args, **kwargs):
        """
        BaseHTMLScraper constructor
        :param url: the url of the fetchers page
        """
        self.logger = logging.getLogger(type(self).__name__)
        self.fetcher = BaseHTMLFetcher(url)
        html = self.fetcher.fetch_content()
        try:
            self.soup = BeautifulSoup(html, 'html.parser')
        except Exception as e:
            self.logger.error(f'Failed to scrape {url}: {e}', exc_info=True)
            raise e

    def get_table_to_map(self, key_header: str, value_header: str) -> Tuple[Tag | None, int | None, int | None]:
        """
        Get table to map based on key and value headers.
        If table found returns method returns the table tag and the key and value headers indexes.
        :param key_header: key header to map
        :param value_header: value header to map
        :return: table tag, key index in table, value index in table, key header, value header
        """
        tables = self.soup.find_all('table')
        for table in tables:
            headers = [th.get_text(strip=True) for th in table.find_all('th')]
            if all(header in headers for header in (key_header, value_header)):
                self.logger.info(f'Found table with key {key_header} and value {value_header} in {self.fetcher.url}')
                return table, headers.index(key_header), headers.index(value_header)

        self.logger.warning(f'No table with key {key_header} and value {value_header} found in {self.fetcher.url}')
        return None, None, None

    def get_image_url(self) -> str:
        """
        Abstract method to get image url, each scraper should implement its own logic
        """
        raise NotImplementedError("get_image_url not implemented")

    def download_image(self, image_name: str, directory: str):
        try:
            ImageDownloader(url=self.get_image_url(), file_name=image_name, directory=directory).download()
        except Exception as e:
            self.logger.error(f"Error downloading image {image_name}: {e}", exc_info=True)
            raise e


class BaseTableScraper:
    """
    Base class for fetchers table scraping
    """
    def __init__(self, table: Tag):
        """
        BaseTableScraper constructor
        :param table: the table tag
        """
        self.table = table

    def rows(self, skip_header: bool = True) -> List[Tag]:
        """
        Return all rows in the table, optionally skipping the header.
        :param skip_header: if true, skip the first row
        :return: list of the table rows as tags
        """
        rows = self.table.find_all('tr')
        return rows[1:] if skip_header else rows

    @staticmethod
    def cells(row: Tag) -> ResultSet:
        """
        Return all <td> or <th> cells in a row.
        :param row:
        :return:
        """
        return row.find_all(['td', 'th'])


class TableMappingScraper(BaseTableScraper):
    """
    Table scraper class to handle general mapping creation from fetchers table.
    The mapping is based on keys and values extractors, given to the class in initialize.
    """
    def __init__(self, table: Tag, keys_extractor: BaseCellsExtractor, values_extractor: BaseCellsExtractor):
        """
        TableMappingScraper constructor
        :param table: the table tag
        :param keys_extractor: the keys extractor
        :param values_extractor: the values extractor
        """
        super().__init__(table=table)
        self.key_extractor = keys_extractor
        self.value_extractor = values_extractor
        self.cells_range = max(keys_extractor.col_idx, values_extractor.col_idx)

    def create_mapping(self) -> Dict[str, List[Dict[str, str]]]:
        """
        Builds a mapping from the keys to the values, using the class given extractors.
        :return: dictionary mapping keys to values
        """
        mapping: Dict[str, List[Dict[str, str]]] = defaultdict(list)
        for row in self.rows():
            cells = self.cells(row)
            if len(cells) <= self.cells_range:
                continue
            keys = self.key_extractor.extract(cells)
            values = self.value_extractor.extract(cells)

            for key in keys:
                mapping[key].extend(values)

        return mapping