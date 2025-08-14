import re
from typing import Tuple

from bs4 import Tag

from components.scrapers.base_scrapers import BaseHTMLScraper


class WikiScraper(BaseHTMLScraper):
    """
    Wikipedia scraper class.
    Implement get_image_url logic specifically for Wikipedia pages.
    """
    def get_image_url(self) -> str | None:
        """
        Get the main image url of a wikipedia page
        :return: the main image url as https url if found, None otherwise.
        """
        for raw_img in self.soup.find_all('img'):
            img_src = raw_img.get('src')
            if re.search('wikipedia/.*/thumb/', img_src) and not re.search('.svg', img_src):
                return "https:" + img_src
        return None

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