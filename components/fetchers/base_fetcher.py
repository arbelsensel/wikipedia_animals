import requests

class BaseHTMLFetcher:
    DEFAULT_AGENT = "Chrome/138.0.0.0 Safari/537.36"
    def __init__(self, url: str, user_aget: str = None, timeout: int = None) -> None:
        self.url = url
        self.user_agent = user_aget or self.DEFAULT_AGENT
        self.timeout = timeout

    def fetch(self):
        try:
            resp = requests.get(self.url, headers={"User-Agent": self.user_agent}, timeout=self.timeout)
            resp.raise_for_status()
            return resp
        except requests.exceptions.RequestException as e:
            raise e

    def fetch_content(self):
        return self.fetch().content
