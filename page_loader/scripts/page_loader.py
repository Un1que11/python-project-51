#!/usr/bin/env python3
from page_loader.cli.cli import parse_args
from page_loader.page_loader.loader import download


def main():
    url_address, output = parse_args()

    print(download(url_address, output))


if __name__ == '__main__':
    main()
