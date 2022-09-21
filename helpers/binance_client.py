from binance.client import Client

from configs.config import API_KEY, API_SECRET

client = Client(API_KEY, API_SECRET)


def get_historical_klines(symbol, target_exchance, interval, max_need):
    print("Collecting Historical Data")
    klines = client.get_historical_klines(symbol=symbol+target_exchance, interval=interval, limit=max_need+1)
    # return 0=open time, 1=open price, 2= High price, 3=Low price, 4= close price, 5= volume
    return klines
