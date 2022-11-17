from decimal import Decimal
import requests
from binance.client import Client
from settings.configs import API_KEY, API_SECRET

client = Client(API_KEY, API_SECRET)


def get_price(symbol):
    key = f'https://api.binance.com/api/v3/ticker/price?symbol={str(symbol).upper()}'
    data = requests.get(key)
    data = data.json()
    price = data['price']
    return float(price)


def get_tick_size(symbol):
    info = client.get_symbol_info(str(symbol).upper())
    tick_size = info["filters"][0]["tickSize"]
    return tick_size


def amount_calc(symbol, budget, buy_price):
    tick_size = get_tick_size(symbol)
    quantity = budget / buy_price

    quantity = Decimal(str(quantity))
    rounded_quantity = float(quantity - quantity % Decimal(str(tick_size)))
    return rounded_quantity, 0


def get_historical_klines(symbol, target_exchange, interval, max_need):
    print("Collecting Historical Data")
    klines = client.get_historical_klines(symbol=symbol + target_exchange, interval=interval,
                                          limit=max_need + 1)  # +1 for pop last data
    # return 0=open time, 1=open price, 2= High price, 3=Low price, 4= close price, 5= volume
    return klines


def get_all_historical_klines(symbol, target_exchange, interval):
    print("Collecting Historical Data")
    start = '2022-01-01'
    klines = client.get_historical_klines(symbol=symbol + target_exchange, interval=interval, start_str=start)
    # return 0=open time, 1=open price, 2= High price, 3=Low price, 4= close price, 5= volume
    return klines


"""
TESTING SECTION
"""


def test_sell(coin_amount, symbol, process_count):
    sell_price = get_price(symbol)
    process_count = process_count + 1

    budget = float(coin_amount) * float(sell_price)

    return float(budget), process_count, 0


def win_rate_calc(win_count, process_count):
    perc = 100 * (win_count / process_count)
    return perc