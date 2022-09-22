from check_db_datas import get_datas
from configs.config import SYMBOLS, INTERVAL, RSIPERIODS, MAPERIODS
import indicators.talib_indicators as indicator

import numpy

def signals():
    for symbol in SYMBOLS:
        open = []
        high = []
        low = []
        close = []
        for data in get_datas(symbol):
            open.append(float(data[1]))
            high.append(float(data[2]))
            low.append(float(data[3]))
            close.append(float(data[4]))

        np_opens = numpy.array(open)
        np_highs = numpy.array(high)
        np_lows = numpy.array(low)
        np_closes = numpy.array(close)


        for rsi_period in RSIPERIODS:
            globals()[f'{symbol}_RSI_{rsi_period}'] = indicator.RSI(np_closes, rsi_period)
            print(f'{symbol}_RSI_{rsi_period}', globals()[f'{symbol}_RSI_{rsi_period}'])

        for ma_periods in MAPERIODS:
            globals()[f'{symbol}_MA_{ma_periods}'] = indicator.MA(np_closes, ma_periods)
            print(f'{symbol}_MA_{ma_periods}', globals()[f'{symbol}_MA_{ma_periods}'])

        print("")