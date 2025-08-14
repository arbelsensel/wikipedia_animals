import logging
import os
from collections import defaultdict
from typing import Tuple, List, Any, Dict

import requests
from bs4 import BeautifulSoup, Tag, ResultSet


class ImageNotFound(Exception):
    pass


class BaseHTMLScraper:
    """
    Base class for html page scrapers
    """
    def __init__(self, url: str):
        """
        BaseHTMLScraper constructor
        :param url: the url of the html page
        """
        self.logger = logging.getLogger(type(self).__name__)
        self.url = url
        try:
            self.soup = BeautifulSoup(requests.get(url).content, 'html.parser')
        except Exception as e:
            raise self.logger.error(f'Failed to scrape {url}: {e}', exc_info=True)

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
                self.logger.info(f'Found table with key {key_header} and value {value_header} in {self.url}')
                return table, headers.index(key_header), headers.index(value_header)

        self.logger.warning(f'No table with key {key_header} and value {value_header} found in {self.url}')
        return None, None, None

    def get_image_url(self) -> str:
        """
        Abstract method to get image url, each scraper should implement its own logic
        """
        raise NotImplementedError("get_image_url not implemented")

    def download_image(self, image_name: str, directory: str):
        try:
            img_url = self.get_image_url()
            if not img_url:
                raise ImageNotFound(f"{image_name} not found in {self.url}")

            file_path = self.get_image_path(img_url, image_name, directory)
            response = requests.get(url=img_url,
                                    headers={
                "User-Agent": "WikipediaAnimalScraper/1.0 (https://example.com/contact)"
            },
                                    timeout=(5, 10))
            response.raise_for_status()  # raises for 4xx/5xx
            if not response.content:
                raise ValueError("Empty content")

            img_data = response.content

            with open(file_path, "wb") as f:
                f.write(img_data)
        except Exception as e:
            self.logger.error(f"Error downloading image {image_name}: {e}", exc_info=True)

    @staticmethod
    def get_image_path(img_url, image_name, directory):
        file_format = os.path.splitext(os.path.basename(img_url))[1]
        file_name = f"{image_name}{file_format}"
        file_path = os.path.join(directory, file_name)

        if os.path.exists(file_path):
            raise FileExistsError(f"File {file_name} already exists in {os.path.dirname(file_path)}")

        return file_path


class BaseCellsExtractor:
    """
    Base class for all table cells extractors
    """
    def __init__(self, col_idx: int):
        """
        BaseCellsExtractor constructor
        :param col_idx: the index of the column to extract in the table
        """
        self.col_idx = col_idx

    def extract(self, cells: ResultSet) -> List[Any]:
        raise NotImplementedError("extract method is not implemented")


class BaseTableScraper:
    """
    Base class for html table scraping
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
    Table scraper class to handle general mapping creation from html table.
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