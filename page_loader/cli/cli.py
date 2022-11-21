import argparse
import os


def parse_args():
    parser = argparse.ArgumentParser(
        description='Downloading web-page to local directory'
    )

    parser.add_argument(
        '--output',
        type=str,
        default=os.getcwd()
    )
    parser.add_argument(
        'url_address',
        type=str
    )

    args = parser.parse_args()
    return args.url_address, args.output
