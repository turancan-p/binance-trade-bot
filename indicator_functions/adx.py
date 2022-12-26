import talib

class AdxCalculator:
    def __init__(self):
        self.adx_datas = dict()

    def calculate(self, symbol, high_datas, low_datas, close_datas, value: int = 12):
        self.adx_datas[symbol] = talib.ADX(high_datas, low_datas, close_datas, value)[-1]