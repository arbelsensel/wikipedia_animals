import logging
import os

from components.fetchers.base_fetcher import BaseHTMLFetcher


class ImageDownloader:
    """
    Class handler for downloading images from a url
    """
    def __init__(self, url: str, file_name: str, directory: str):
        self.logger = logging.getLogger(__name__)
        self.url = url
        self.file_path = self.set_file_path(file_name, directory)

    def download(self, retries: int = 3):
        """
        Download the image from the url, retries mechanism implemented
        :param retries: amount of times to retry download before raising exception
        """
        try:
            for attempt in range(1, retries + 1):
                try:
                    response = BaseHTMLFetcher(url=self.url, timeout=10).fetch()
                    if not response.content:
                        raise ValueError("Empty content")

                    img_data = response.content
                    with open(self.file_path, "wb") as f:
                        f.write(img_data)

                    self.logger.info(f"Image downloaded successfully to: {self.file_path}")

                    break

                except Exception as e:
                    self.logger.error(f"Attempt {attempt} | Error downloading image: {e}", exc_info=True)

        except Exception as e:
            self.logger.error(f"All retries ({retries}) failed | Error downloading image: {e}", exc_info=True)
            raise e

    def set_file_path(self, file_name: str, directory: str) -> str:
        """
        Set the file path given the file name and directory
        :param file_name: file name to download
        :param directory: directory path to download
        :return: the full file path
        """
        file_format = os.path.splitext(os.path.basename(self.url))[1]
        file_name = f"{file_name}{file_format}"
        file_path = os.path.join(directory, file_name)

        if os.path.exists(file_path):
            self.logger.error(f"Failed to set file path {file_path} to {file_name}, file already exists")
            raise FileExistsError(f"File {file_name} already exists in {os.path.dirname(file_path)}")

        self.logger.info(f"File {file_name} will be saved to: {file_path}")

        return file_path
