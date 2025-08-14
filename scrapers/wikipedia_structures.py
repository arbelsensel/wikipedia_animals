import re
from typing import List, Dict
from bs4 import ResultSet

from scrapers.base_scrapers import BaseCellsExtractor, BaseHTMLScraper
from utils import clean_str


class AnimalExtractor(BaseCellsExtractor):
    """
    Extractor class to extract  animals from Wikipedia table cells.
    """
    def extract(self, cells: ResultSet) -> List[Dict[str, str]]:
        """Extracts the animal name and href from a cell containing an <a> tag."""
        a_tag = cells[self.col_idx].find('a')
        if not a_tag or not a_tag.text.strip():
            return []
        return [{"name": clean_str(a_tag.text), "href": a_tag.get("href", "")}]

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

