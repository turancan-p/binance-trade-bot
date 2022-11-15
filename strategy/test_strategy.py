import numpy
import talib
import threading

from settings.configs import SYMBOLS, TARGET_EXCHANCE
from sqlite3_db.get_data_from_db import datas_for_signal


def signal_finder(symb):
    global numpy_closes
    global last_signals

    last_signals = {}
    close_values = []

    dataframe = datas_for_signal(symb)
    for x in range(1, len(dataframe)):
        data_index = dataframe[x:x + 1]
        close_value = float(data_index['Close'])
        close_values.append(close_value)
        numpy_closes = numpy.array(close_values)

    rsi_20 = talib.RSI(numpy_closes, 20)

    last_rsi_20 = rsi_20[-1]
    ema_50 = talib.EMA(numpy_closes, 50)
    last_ema_50 = ema_50[-1]
    ema_100 = talib.EMA(numpy_closes, 100)
    last_ema_100 = ema_100[-1]

    if last_rsi_20 < 30:
        last_signals[symb] = "BUY"
    elif last_rsi_20 > 70:
        last_signals[symb] = "SELL"
    else:
        last_signals[symb] = "WAIT"
    print(f'SYMBOL: {symb+TARGET_EXCHANCE} RSI_20: {last_rsi_20} EMA_50: {last_ema_50} EMA_100: {last_ema_100}')
    return last_signals[symb]


def run_strategy():
    signals = {}
    for symbol in SYMBOLS:
        signals[symbol+TARGET_EXCHANCE] = signal_finder(symbol)
    print("")
    return signals