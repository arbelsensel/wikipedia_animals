from main import download_image
import urllib.parse as urlparse
import os
import tempfile

URL_PREFIX = "https://en.wikipedia.org"
# test_dict = {
#             "url": urlparse.urljoin(URL_PREFIX, "/wiki/Gnat"),
#             "image_name": "Gnat",
#             "directory": tmpdir
#         }

def test_download_image():
    with tempfile.TemporaryDirectory() as tmpdir:
        test_dict = {
            "url": urlparse.urljoin(URL_PREFIX, "/wiki/Cockroach"),
            "image_name": "Cockroach",
            "directory": tmpdir
        }

        download_image(**test_dict)

        assert(os.path.exists(os.path.join(tmpdir, f"{test_dict['image_name']}.png"))), f"{test_dict['image_name']} image is not downloaded"


