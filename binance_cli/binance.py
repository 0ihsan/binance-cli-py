"""binance-py - binance scraper, streamer

Usage:
  binance-py status
  binance-py balance
  binance-py order --amount
  binance-py (-h | --help)
  binance-py --version

Options:
  -h --help                 Show this screen.
  --version                 Show the version."""

from docopt import docopt
from binance.client import Client
from json import dumps
from sys import stdout, stderr, exit

version = '0.0.1'


def main():

    arg = docopt(__doc__, version=version)

    print(arg)

    if arg['--help']:
        print(__doc__, file=stderr)
        return(0)

    else:
        print(__doc__, file=stderr)
        return(1)


if __name__ == '__main__':
    exit(main())
