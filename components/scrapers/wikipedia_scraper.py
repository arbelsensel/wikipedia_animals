import re

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

