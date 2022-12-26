import talib

class EmaCalculator:
    def __init__(self):
        self.ema_datas = dict()

    def calculate(self, symbol, close_datas, value: int):
        self.ema_datas[symbol] = talib.EMA(close_datas, value)[-1]