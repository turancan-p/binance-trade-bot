import talib

class AtrCalculator:
    def __init__(self):
        self.atr_datas = dict()

    def calculate(self, symbol, high_datas, low_datas, close_datas, value: int):
        self.atr_datas[symbol] = talib.ATR(high_datas, low_datas, close_datas, value)[-1]