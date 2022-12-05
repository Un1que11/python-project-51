import pytest
from page_loader.page_loader import parser


TEST_CASES = [
    ('https://ru.test.com/test.js', 'https://ru.test.com', True),
    ('https://cdn.test.com/test.js', 'https://ru.test.com', False),
]


@pytest.mark.parametrize('full_url, url, expected_result', TEST_CASES)
def test_is_local(full_url, url, expected_result):
    test_result = parser.is_local(full_url, url)
    assert test_result == expected_result
