from binance_functions.functions import get_all_historical_klines
from settings.configs import SYMBOLS, INTERVAL, TARGET_EXCHANCE
import csv

header = ['Symbol', 'Open', 'High', 'Low', 'Close']


def collect():
    for symbol in SYMBOLS:
        datas = get_all_historical_klines(symbol, TARGET_EXCHANCE, INTERVAL)
        datas.pop()
        with open(f'{symbol}@kline_{INTERVAL}.csv', mode='w', newline='') as f:
            writer = csv.writer(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            writer.writerow(header)
            for data in datas:
                openp = data[1]
                highp = data[2]
                lowp = data[3]
                closep = data[4]
                new_Data = [symbol, openp, highp, lowp, closep]
                writer.writerow(new_Data)

collect()