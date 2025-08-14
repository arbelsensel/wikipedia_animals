import requests

class BaseHTMLFetcher:
    """
    Base class for fetching HTML pages.
    """

    DEFAULT_AGENT = "Chrome/138.0.0.0 Safari/537.36"

    def __init__(self, url: str, user_aget: str = None, timeout: int = None) -> None:
        """
        BaseHTMLFetcher constructor.
        :param url: URL to fetch.
        :param user_aget: User-agent string to use for fetching.
        :param timeout: Timeout in seconds for the request
        """
        self.url = url
        self.user_agent = user_aget or self.DEFAULT_AGENT
        self.timeout = timeout

    def fetch(self):
        """
        fetch HTML page.
        :return: response
        """
        try:
            resp = requests.get(self.url, headers={"User-Agent": self.user_agent}, timeout=self.timeout)
            resp.raise_for_status()
            return resp
        except requests.exceptions.RequestException as e:
            raise e

    def fetch_content(self):
        """
        fetch HTML page content.
        :return: the response content
        """
        return self.fetch().content
