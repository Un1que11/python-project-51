import tempfile
import os
import requests_mock
import pytest

from page_loader.page_loader import loader


TEST_URL = 'https://test.com'


@pytest.fixture()
def create_test_url(requests_mock):
    requests_mock.get(TEST_URL, text='data')


def test_download_with_path(create_test_url):
    with tempfile.TemporaryDirectory() as test_path:
        expected = os.path.join(test_path, 'test-com.html')
        test_func_res = loader.download(TEST_URL, test_path)
        assert test_func_res == expected


def test_download_without_path(create_test_url):
    expected = os.path.join(os.getcwd(), 'test-com.html')
    test_func_res = loader.download(TEST_URL)
    assert test_func_res == expected
