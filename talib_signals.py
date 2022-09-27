from check_db_datas import get_datas
from configs.config import SYMBOLS, INTERVAL
import indicators.talib_indicators as indicator
from helpers.binance_client import create_market_order, get_orders

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

        # STRATEGY

        golden_cross = False

        if not golden_cross and indicator.EMA(np_closes, 50) > indicator.EMA(np_closes, 200):
            golden_cross = True
            if indicator.RSI(np_closes, 14) < 30:
                print("BUYING!", symbol)

                # print(create_market_order(symbol, "BUY", 0, 0))

        if golden_cross and indicator.EMA(np_closes, 50) < indicator.EMA(np_closes, 200):
            if indicator.RSI(np_closes, 14) > 70:
                print("SELLING!", symbol)

                # print(create_market_order(symbol, "SELL", 0, 0))
