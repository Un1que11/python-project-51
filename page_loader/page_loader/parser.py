import os
from typing import Any
from urllib.parse import urljoin, urlparse

from bs4 import BeautifulSoup
from page_loader.page_loader.file_path_work import get_file_name

ATTRIBUTES = {
    'img': 'src',
    'link': 'href',
    'script': 'src',
}


def data_parse(
    page: Any,
    url: str,
    files_dir: str,
) -> tuple[str, dict]:
    upd_files_paths = {}
    soup = BeautifulSoup(page, 'html.parser')
    tags = soup.find_all(ATTRIBUTES)

    for tag in tags:
        name = ATTRIBUTES[tag.name]
        url_to_media = tag.get(name)
        full_url = urljoin(url, url_to_media)

        if is_local(full_url, url):
            local_file_name = get_file_name(full_url)
            upd_files_paths[full_url] = local_file_name
            tag[name] = os.path.join(files_dir, local_file_name)

    updated_page = soup.prettify()
    return updated_page, upd_files_paths


def is_local(full_url: str, url: str) -> bool:
    return urlparse(full_url).netloc == urlparse(url).netloc
