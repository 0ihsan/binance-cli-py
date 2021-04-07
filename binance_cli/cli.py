"""binance-cli - manage your binance account in command line

Usage:
  binance-cli status
  binance-cli order --amount
  binance-cli balance (spot | futures | coin) [ --hide-zero ]
  binance-cli show (spot | futures | coin) orders
  binance-cli (-h | --help)
  binance-cli --version

Options:
  --hide-zero               Do not show zero balances.
  -h --help                 Show this screen.
  --version                 Show the version."""

from binance.client import Client
from docopt import docopt
from json import dumps
from os import getenv
from sys import stdout, stderr, exit

version = '0.1.0'


def main():

    arg = docopt(__doc__, version=version)
    api_key = getenv('BINANCE_FUTURES_API')
    sec_key = getenv('BINANCE_FUTURES_SEC')
    if not api_key and not sec_key:
        print('please set these environment variables:\n'\
              '    BINANCE_FUTURES_API\n'\
              '    BINANCE_FUTURES_SEC', file=stderr)
        return 1
    if not api_key:
        print('environment variable not found: BINANCE_FUTURES_API',file=stderr)
        return 1
    if not sec_key:
        print('environment variable not found: BINANCE_FUTURES_SEC',file=stderr)
        return 1
    client = Client(api_key, sec_key)

    if arg['--help']:
        print(__doc__, file=stderr)
        return 0

    elif arg['status']:
        return client.get_system_status()['status']

    elif arg['balance']:
        if arg['futures']:
            print(dumps(client.futures_account_balance()))
        elif arg['spot']:
            print(dumps(client.get_account()['balances']))
        elif arg['coin']:
            print(dumps(client.futures_coin_account_balance()))
        return 0

    elif arg['show']:
        if arg['spot']:
            if arg['orders']:
                # if arg['--all']:
                #     print(dumps(client.get_all_orders()))
                # else:
                print(dumps(client.get_open_orders()))


    else:
        print(__doc__, file=stderr)
        return 1


if __name__ == '__main__':
    exit(main())
