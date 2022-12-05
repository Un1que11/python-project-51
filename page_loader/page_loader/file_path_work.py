import os
import re
from urllib.parse import urlparse

FOLDER_NAME = '_files'
HTML_EXT = '.html'


def get_file_name(url: str) -> str:
    file_name, ext = get_file_name_and_ext(url)
    if ext:
        return file_name + ext
    return file_name + HTML_EXT


def get_directory_name(url: str) -> str:
    file_name, _ = get_file_name_and_ext(url)
    return file_name + FOLDER_NAME


def get_file_name_and_ext(url: str) -> tuple:
    parsed_url = urlparse(url)
    root, ext = os.path.splitext(parsed_url.path)
    url_without_scheme = os.path.join(parsed_url.netloc + root)
    file_name = re.sub(r'[^\w]', '-', url_without_scheme.rstrip('/'))
    return file_name, ext
