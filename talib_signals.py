from check_db_datas import get_datas
from configs.config import SYMBOLS, INTERVAL
import indicators.talib_indicators as indicator

import numpy


def signals():
    print("Waiting for Signal!")
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

        golden_cross = False

        if not golden_cross and indicator.EMA(np_closes, 50) > indicator.EMA(np_closes, 200):
            golden_cross = True
            if indicator.RSI(np_closes, 14) < 30:
                print("BUYING!", symbol)
        if golden_cross and indicator.EMA(np_closes, 50) < indicator.EMA(np_closes, 200):
            if indicator.RSI(np_closes, 14) > 70:
                print("SELLING!", symbol)

        # for rsi_period in RSIPERIODS:
        #     globals()[f'{symbol}_RSI_{rsi_period}'] = indicator.RSI(np_closes, rsi_period)
        #     # print(f'{symbol}_RSI_{rsi_period}', globals()[f'{symbol}_RSI_{rsi_period}'])
        #
        # for ma_periods in MAPERIODS:
        #     globals()[f'{symbol}_MA_{ma_periods}'] = indicator.MA(np_closes, ma_periods)
        #     # print(f'{symbol}_MA_{ma_periods}', globals()[f'{symbol}_MA_{ma_periods}'])
        #
        # for ema_periods in EMAPERIODS:
        #     globals()[f'{symbol}_EMA_{ema_periods}'] = indicator.EMA(np_closes, ema_periods)
        #
        # for adx_periods in ADXPERIODS:
        #     globals()[f'{symbol}_ADX_{adx_periods}'] = indicator.ADX(np_highs, np_lows, np_closes, adx_periods)
        #     # print(f'{symbol}_ADX_{adx_periods}', globals()[f'{symbol}_ADX_{adx_periods}'])
        #
        # for bbands_periods in BBANDSPERIODS:
        #     globals()[f'{symbol}_BBAND_{bbands_periods}'] = indicator.BBANDS(np_closes, bbands_periods)
        #     # print(f'{symbol}_BBAND_{bbands_periods}', globals()[f'{symbol}_BBAND_{bbands_periods}'])