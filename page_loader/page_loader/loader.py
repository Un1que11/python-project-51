import logging
import os
import traceback
from typing import Union
import requests
from progress.bar import IncrementalBar

from page_loader.page_loader.exceptions import FileSystemError, NetworkError
from page_loader.page_loader.parser import data_parse
from page_loader.page_loader.file_path_work import \
    get_file_name, \
    get_directory_name


SUCCESS_MSG = 'Successfully downloaded: {0}'
FAIL_MSG = 'Failed to download: {0} \n{1}'
DENY_MSG = 'Permission to {0} denied.'
GOT_CONTENT_MSG = 'Got content from {0}'
STATUS_MSG = 'URL: {0}, status code: {1}'

logger = logging.getLogger(__name__)


def download(
        url: str,
        dir_path: str
) -> str:
    page = get_content(url)
    local_page_name = get_file_name(url)
    local_page_path = os.path.join(dir_path, local_page_name)
    local_files_path = get_directory_name(url)
    updated_page, upd_files_paths = data_parse(
        page,
        url,
        local_files_path,
    )
    local_page_path = save(local_page_path, updated_page)

    if upd_files_paths:
        download_updated_files(dir_path, local_files_path, upd_files_paths)

    return local_page_path


def save(
        local_path: str,
        resource: Union[bytes, str],
        mode='w'
) -> str:
    try:
        with open(local_path, mode=mode) as out:
            out.write(resource)
    except IOError as exc:
        logger.debug(traceback.format_exc(8))
        logger.error(DENY_MSG.format(local_path))
        raise FileSystemError from exc
    logger.debug(SUCCESS_MSG.format(local_path))
    return local_path


def download_resources(
        files_path: dict,
        dir_path: str
) -> None:
    with IncrementalBar(
            'In Progress',
            max=len(files_path),
            suffix='%(percent)d%%',
    ) as progress_bar:
        for url, local_name in files_path.items():
            try:
                resource = get_content(url)
                local_path = os.path.join(dir_path, local_name)
                save(local_path, resource, 'wb')
                progress_bar.next()
            except requests.exceptions.RequestException:
                logger.debug(traceback.format_exc(2, chain=False))
                logger.error(FAIL_MSG.format(
                    url,
                    traceback.format_exc(0, chain=False),
                ))


def download_updated_files(
    dir_path: str,
    local_files_path: str,
    upd_files_paths: dict,
) -> None:
    dir_path = os.path.join(dir_path, local_files_path)
    os.makedirs(dir_path, exist_ok=True)
    download_resources(upd_files_paths, dir_path)


def get_content(url: str) -> bytes:
    response = requests.get(url)

    try:
        response.raise_for_status()
    except requests.exceptions.RequestException as exp:
        logger.debug(traceback.format_exc(2, chain=False))
        logger.error(FAIL_MSG.format(
            url,
            traceback.format_exc(0, chain=False),
        ))
        raise NetworkError from exp

    logger.debug(GOT_CONTENT_MSG.format(url))
    return response.content
