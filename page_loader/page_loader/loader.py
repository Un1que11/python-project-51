import os
import re
import requests


def download(url_address, output=os.getcwd()):
    r = requests.get(url_address) # noqa F841

    if url_address.startswith('https://'):
        url_address = url_address[8:]
    else:
        url_address = url_address[7:]

    url_address = re.sub(r'[^a-zA-Z0-9]', r'-', url_address)
    file_name = os.path.join(output, url_address)
    file_name = file_name + '.html'

    return file_name
