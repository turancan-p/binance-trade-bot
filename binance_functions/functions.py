from binance.client import Client
from settings.configs import API_KEY, API_SECRET

client = Client(API_KEY, API_SECRET)


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


def test_buy(budget, buy_price):
    coin_amount = budget / buy_price
    return coin_amount


def test_sell(coin_amount, sell_price, process_count):
    process_count = process_count + 1

    budget = coin_amount * sell_price

    return budget, process_count


def win_rate_calc(win_count, process_count):
    perc = 100 * (win_count / process_count)
    return perc