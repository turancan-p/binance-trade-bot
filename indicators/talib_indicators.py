import talib


def RSI(np_closes, period):
    rsi = talib.RSI(np_closes, period)
    return rsi[-1]


def EMA(np_closes, period):
    ema = talib.EMA(np_closes, period)
    return ema[-1]


def MA(np_closes, period):
    ma = talib.MA(np_closes, period)
    return ma[-1]


def ADX(np_high, np_low, np_close, period):
    adx = talib.ADX(np_high, np_low, np_close, period)
    return adx[-1]


def BBANDS(np_closes, period):
    bbands = talib.BBANDS(np_closes, period)
    return bbands[-1]
