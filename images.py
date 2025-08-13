from venv import logger

import requests
from bs4 import BeautifulSoup
import os
import logging

logging.basicConfig(level=logging.ERROR)

# Wikipedia page URL
URL_PREFIX = "https://en.wikipedia.org"

# Get page HTML
def download_image(url: str, image_name: str):
    try:
        url = URL_PREFIX + url
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")
        infobox = soup.find("table", {"class": "infobox"})
        img_tag = infobox.find("img")
        img_url = "https:" + img_tag["src"]

        # Full path to save the image
        repo_dir = os.path.dirname(os.path.abspath(__file__))

        # Path to tmp folder inside the repo
        tmp_dir = os.path.join(repo_dir, "tmp")
        file_format = os.path.splitext(os.path.basename(img_url))[1]
        filename = os.path.join(tmp_dir, f"{image_name}{file_format}")

        # assert file doesn't exists
        if os.path.exists(filename):
            raise FileExistsError(f"Image {image_name} already exists")

        # Download and save
        img_data = requests.get(img_url).content
        with open(filename, "wb") as f:
            f.write(img_data)

    except Exception as e:
        logging.error(f"Error downloading image {image_name}: {e}", exc_info=True)
