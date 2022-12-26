from statistics import mean

class TrendFinder:
    def __init__(self):
        self.trend = dict()

    def calculate(self, symbol, atr, atr_multiplier, high_datas, low_datas, back_period):
        __low_lenght = len(low_datas)
        __high_lenght = len(high_datas)

        __lowest_price = min(low_datas[__low_lenght - back_period:])
        __highest_price = max(high_datas[__high_lenght - back_period:])

        __short_stop = __lowest_price + (atr_multiplier * atr)
        __long_stop = __highest_price - (atr_multiplier * atr)

        trend_line = mean([__short_stop, __long_stop])

        self.trend[symbol] = {"trend_line": trend_line}


