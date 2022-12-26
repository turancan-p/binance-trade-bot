

class KeltnerChannel:
    def __init__(self):
        self.up_line = dict()
        self.middle_line = dict()
        self.down_line = dict()

    def calculate(self, symbol, atr, ema, atr_multiplier):
        self.up_line[symbol] = ema + (atr * atr_multiplier)
        self.middle_line[symbol] = ema
        self.down_line[symbol] = ema - (atr * atr_multiplier)