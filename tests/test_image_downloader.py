from unittest.mock import patch, Mock

import pytest

from components.fetchers.image_downloader import ImageDownloader
import os
import tempfile

from tests.tests_data.test_data import test_image_path


@patch("components.fetchers.image_downloader.BaseHTMLFetcher.fetch")
def test_download_image(mock_fetch):
    with open(test_image_path, 'rb') as f:
        image_bytes = f.read()
    mock_response = Mock()
    mock_response.content = image_bytes
    mock_fetch.return_value = mock_response

    with tempfile.TemporaryDirectory() as tmpdir:
        ImageDownloader(url="mock", directory=tmpdir, file_name="test.png").download()
        assert os.path.exists(os.path.join(tmpdir, "test.png")), \
            f"ImageDownloader failed to create the file {os.path.join(tmpdir, 'test.png')}"


@patch("components.fetchers.image_downloader.BaseHTMLFetcher.fetch")
def test_download_image_empty_content(mock_fetch):
    mock_response = Mock()
    mock_response.content = None
    mock_fetch.return_value = mock_response

    with tempfile.TemporaryDirectory() as tmpdir:
        with pytest.raises(ValueError):
            ImageDownloader(url="mock", directory=tmpdir, file_name="test.png").download()




