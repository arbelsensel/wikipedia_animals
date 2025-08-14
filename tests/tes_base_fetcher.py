import pytest
import requests

from components.fetchers.base_fetcher import BaseHTMLFetcher

good_url = 'https://google.com'
bad_url = 'https://notexistingblabla.com'

def test_fetch():
    fetcher = BaseHTMLFetcher(url=good_url)
    response = fetcher.fetch()
    assert response.status_code == 200, f"response status code should be 200, instead got {response.status_code}"

def test_fetch_content():
    fetcher = BaseHTMLFetcher(url=good_url)
    content = fetcher.fetch_content()
    assert content is not None, "content is None"

def test_fetch_bad_url():
    fetcher = BaseHTMLFetcher(url=bad_url)
    with pytest.raises(requests.exceptions.ConnectionError):
        fetcher.fetch()