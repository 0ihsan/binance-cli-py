"""binance-cli - binance scraper, streamer

Usage:
  binance-cli status
  binance-cli balance
  binance-cli order --amount
  binance-cli (-h | --help)
  binance-cli --version

Options:
  -h --help                 Show this screen.
  --version                 Show the version."""

from binance.client import Client
from docopt import docopt
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
