from settings.configs import TARGET_EXCHANCE, INTERVAL, HIST_MAX_NEED, SYMBOLS
from sqlite3_db.database import create_db, insert_new_data
from binance_functions.functions import get_historical_klines


def collect():
    for symbol in SYMBOLS:
        create_db(symbol, INTERVAL)
        datas = get_historical_klines(symbol, TARGET_EXCHANCE, INTERVAL, HIST_MAX_NEED)
        datas.pop()

        for data in datas:
            open = data[1]
            high = data[2]
            low = data[3]
            close = data[4]
            new_Data = [open, high, low, close]
            insert_new_data(f'{symbol}{TARGET_EXCHANCE}', INTERVAL, new_Data)
