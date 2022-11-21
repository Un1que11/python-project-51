import pytest
from page_loader.cli.cli import parse_args


def test_cli_without_arg():
    with pytest.raises(SystemExit):
        parse_args()
        pytest.fail()
