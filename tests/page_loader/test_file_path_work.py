import pytest
from page_loader.page_loader import file_path_work


TEST_TEMPLATE = [
    ['https://en.wikipedia.org/Python', 'en-wikipedia-org-Python.html'],
    ['https://en.wikipedia.org/Python.js', 'en-wikipedia-org-Python.js'],
]


@pytest.mark.parametrize('test_case, expected_result', TEST_TEMPLATE)
def test_get_file_name(test_case, expected_result):
    test_result = file_path_work.get_file_name(test_case)
    assert test_result == expected_result


def test_get_folder_name():
    test_result = file_path_work.get_directory_name('https://en.wikipedia.org/Python')
    expected_result = 'en-wikipedia-org-Python_files'
    assert test_result == expected_result
