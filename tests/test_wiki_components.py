import logging
from unittest.mock import patch

from bs4 import BeautifulSoup

from components.fetchers.base_fetcher import BaseHTMLFetcher
from components.scrapers.wikipedia_scraper import WikiScraper
from tests.tests_data.test_data import mock_wiki_html, img_url, mock_html_table, mock_html_table_headers


@patch("components.scrapers.base_scrapers.BaseHTMLScraper.__init__", return_value=None)
def test_wiki_scraper_get_image_url(mock_init):
    scraper = WikiScraper(url="https://some_wikipedia_url")
    scraper.logger = logging.getLogger()
    scraper.soup = BeautifulSoup(mock_wiki_html, "html.parser")

    url = scraper.get_image_url()

    assert url == f"https:{img_url}", f"Should return {img_url}, instead got {url}"

@patch("components.scrapers.base_scrapers.BaseHTMLScraper.__init__", return_value=None)
def test_wiki_scraper_get_table_to_map(mock_init):
    scraper = WikiScraper(url="https://some_wikipedia_url")
    scraper.logger = logging.getLogger()
    scraper.soup = BeautifulSoup(mock_html_table, "html.parser")
    scraper.fetcher = BaseHTMLFetcher(url="https://some_wikipedia_url")

    table, key_idx, value_idx = scraper.get_table_to_map(key_header=mock_html_table_headers[0],
                                                        value_header=mock_html_table_headers[1])

    assert table is not None, "Should return table, got None"
    assert key_idx == 0, f"Should return 0, instead got {key_idx}"
    assert value_idx == 1, f"Should return 1, instead got {value_idx}"


