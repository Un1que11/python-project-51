import pytest
import tempfile
import requests_mock

from page_loader.page_loader.loader import download
from page_loader.page_loader.exceptions import FileSystemError, NetworkError


TEST_URL = 'https://test.com'

STATUS_CODES = [
    pytest.param(
        102,
        marks=pytest.mark.xfail,
    ),
    pytest.param(
        200,
        marks=pytest.mark.xfail,
    ),
    pytest.param(
        303,
        marks=pytest.mark.xfail,
    ),
    404,
    503,
]


def test_download_error(requests_mock):
    requests_mock.get(TEST_URL)
    with pytest.raises(FileSystemError):
        download(TEST_URL, '/directory/doesnt/exist')


@pytest.mark.parametrize('test_code', STATUS_CODES)
def test_download_network_error(test_code):
    with requests_mock.Mocker() as mock:
        mock.get(TEST_URL, status_code=test_code)
        with tempfile.TemporaryDirectory() as test_path:
            with pytest.raises(NetworkError):
                download(TEST_URL, test_path)
