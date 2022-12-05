import tempfile
import os
import requests
import requests_mock
import pytest

from page_loader.page_loader.loader import download, save, get_content


TEST_URL = 'http://test.com'
TEST_PAGE = os.path.join(os.getcwd(), 'tests/fixtures/test_page.html')
TEST_IMG = os.path.join(os.getcwd(), 'tests/fixtures/content/test_image.png')
TEST_CSS = os.path.join(os.getcwd(), 'tests/fixtures/content/test_style.css')
TEST_JS = os.path.join(os.getcwd(), 'tests/fixtures/content/test_script.js')
EXPECTED_PAGE = os.path.join(os.getcwd(), 'tests/fixtures/expected_result.html')


@pytest.fixture()
def test_url_without_content(requests_mock):
    requests_mock.get(TEST_URL, text='<html>\n</html>')


@pytest.fixture()
def test_url_with_content(requests_mock):
    requests_mock.get(TEST_URL, text=open(TEST_PAGE).read())
    requests_mock.get(
        'http://test.com/content/test_style.css',
        body=open(TEST_CSS, 'rb')
    )
    requests_mock.get(
        'http://test.com/content/test_script.js',
        body=open(TEST_JS, 'rb')
    )
    requests_mock.get(
        'http://test.com/content/test_img.png',
        body=open(TEST_IMG, 'rb')
    )


@pytest.fixture()
def expected_test_result(requests_mock):
    requests_mock.get(
        'http://expected.html',
        text=open(EXPECTED_PAGE).read()
    )


def test_download_without_content(test_url_without_content):
    with tempfile.TemporaryDirectory() as test_path:
        expected = os.path.join(test_path, 'test-com.html')
        test_func_res = download(TEST_URL, test_path)
        with open(test_func_res, 'r') as f:
            assert f.read() == requests.get(TEST_URL).text
    assert test_func_res == expected


def test_download_with_content(
        test_url_with_content,
        expected_test_result
):
    with tempfile.TemporaryDirectory() as test_path:
        path = test_path
        page_path = download(TEST_URL, path)
        with open(page_path, 'r') as test_file:
            test_folder = os.path.join(path, 'test-com_files')
            assert len(os.listdir(test_folder)) == 3
            assert open(EXPECTED_PAGE).read() == test_file.read()


def test_save():
    with tempfile.TemporaryDirectory() as test_path:
        expected_test_path = os.path.join(test_path, 'save')
        result_test_path = save(expected_test_path, 'hello')
        with open(result_test_path, 'r') as test_file:
            assert test_file.read() == 'hello'
    assert result_test_path == expected_test_path


def test_get_content():
    with requests_mock.Mocker() as mock:
        test_content = 'bytestring'.encode()
        mock.get(TEST_URL, content=test_content)
        assert get_content(TEST_URL) == test_content
