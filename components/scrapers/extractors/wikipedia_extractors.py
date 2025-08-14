from typing import List, Tuple

from bs4 import ResultSet

import urllib.parse as urlparse
from components.scrapers.extractors.base_extractor import BaseCellsExtractor
from utils import clean_str


class AnimalExtractor(BaseCellsExtractor):
    """
    Extractor class to extract  animals from Wikipedia table cells.
    """

    URL_PREFIX = "https://en.wikipedia.org"

    def extract(self, cells: ResultSet) -> List[Tuple[str, str]]:
        """Extracts the animal name and href from a cell containing an <a> tag.
        :param cells: cells to extract animals from.
        :return: list of (animal, href) tuples.
        """
        a_tag = cells[self.col_idx].find('a')
        if not a_tag or not a_tag.text.strip():
            return []
        return [(clean_str(a_tag.text), urlparse.urljoin(self.URL_PREFIX, a_tag.get("href", "")))]


class CollateralAdjectivesExtractor(BaseCellsExtractor):
    """
    Extractor class to extract collateral adjectives from Wikipedia table cells.
    """
    def extract(self, cells: ResultSet) -> List[str]:
        """Extracts collateral adjectives from a table cell."""
        cell_text = cells[self.col_idx].get_text(separator="\n")
        adjectives = [
            clean_str(p.strip())
            for p in cell_text.split("\n")
            if p.strip() and p.strip() != "—" and len(p.strip()) > 1
        ]
        return adjectives or ["Null"]
