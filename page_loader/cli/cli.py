import argparse
import os

DEFAULT_DIR = os.getcwd()


def parse_args():
    parser = argparse.ArgumentParser(
        prog='page-loader',
        usage='page-loader [options] <url>',
        description='Downloading web-page to local directory',
        add_help=False,
    )
    parser.add_argument(
        '-o',
        '--output',
        action='store',
        default=DEFAULT_DIR,
        help='output dir (default: "{0}")'.format(DEFAULT_DIR),
        type=str,
    )
    parser.add_argument(
        '-v',
        '--version',
        action='version',
        version='page-loader 0.4.0',
    )
    parser.add_argument(
        '-h',
        '--help',
        action='help',
        help='dispaly help for command',
    )
    parser.add_argument(
        'url',
        help='url to download',
        type=str,
    )
    args = parser.parse_args()
    return args.url, args.output
