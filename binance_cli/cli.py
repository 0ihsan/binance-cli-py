"""binance-cli - manage your binance account in command line

Usage:
  binance-cli (-h | --help)
  binance-cli --version
  binance-cli balance (spot | futures | coin) [ -z | --hide-zero ] [ -v | --verbose]
  binance-cli order <side> <quantity> <symbol> (--limit <price> | --market) [ --tif <tif> ] [ --test ] [ -v | --verbose ]
  binance-cli show (spot | futures | coin) orders [ -v | --verbose ]
  binance-cli status [ -v | --verbose ]

Options:
  --tif <tif>         Time in force. Either gtc, ioc or fok. [default: gtc]
  --version           Show the version.
  -h --help           Show this screen.
  -l --limit <price>  Set limit price for order.
  -m --market         Buy directly from the market price.
  -t --test           Test instead of actually do.
  -v --verbose        Verbose output, enable debug messages.
  -z --hide-zero      Do not show zero balances."""

from binance.client import Client
from docopt import docopt
from json import dumps
from os import getenv
from sys import stdout, stderr, exit
import sys

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
    sides = {
        'buy': Client.SIDE_BUY,
        'long':  Client.SIDE_BUY,
        'sell':  Client.SIDE_SELL,
        'short':  Client.SIDE_SELL,
    }
    types = {
        'limit': Client.ORDER_TYPE_LIMIT,
        'market': Client.ORDER_TYPE_MARKET
    }
    tifs = {
        'gtc': Client.TIME_IN_FORCE_GTC,
        'ioc': Client.TIME_IN_FORCE_IOC,
        'fok': Client.TIME_IN_FORCE_FOK
    }

    if arg['--verbose']:
        print(arg, file=stderr)
    else:
        sys.tracebacklimit = 0

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

    elif arg['order']:
        tif = tifs[arg['--tif']]
        symbol = arg['<symbol>'].upper()
        if arg['<side>'].strip().lower() in sides:
            side = sides[arg['<side>'].strip().lower()]
        else:
            print('error: side should be either "buy|long" or "sell|short"'\
                  ' not', arg['side'], file=stderr)
        quantity = float(arg['<quantity>'])
        if arg['--limit']:
            if arg['--limit']:
                price = float(arg['--limit'])
                type_ = types['limit']
                if arg['--test']:
                    client.create_test_order(symbol=symbol,
                                             side=side,
                                             quantity=quantity,
                                             price=price,
                                             timeInForce=tif,
                                             type=type_)
                else: # actually send the order
                    client.create_order(symbol=symbol,
                                        side=side,
                                        quantity=quantity,
                                        price=price,
                                        timeInForce=tif,
                                        type=type_)
            else:
                print('please provide --limit \033[33m<price>\033[0m.')
        elif arg['--market']:
            type_ = types['market']
            if arg['--test']:
                client.create_test_order(symbol=symbol,
                                         side=side,
                                         quantity=quantity,
                                         type=type_)
            else: # actually send the order
                client.create_order(symbol=symbol,
                                    side=side,
                                    quantity=quantity,
                                    type=type_)
        else:
            print('please provide either '\
                  '\033[33m --limit <price>\033[0m '\
                  'or \033[33m--market\033[0m', file=stderr)

    else:
        print(__doc__, file=stderr)
        return 1


if __name__ == '__main__':
    exit(main())
