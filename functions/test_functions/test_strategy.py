from functions.indicator_functions.rsi import RsiCalculator


class TestStrategy():
    def __init__(self):
        self.rsi = RsiCalculator()
        

    def strategy(self):
        self.rsi.calculate_rsi_datas(20)
        __min_rsi_symbol, __min_rsi_value = self.rsi.min_rsi()
        if __min_rsi_value < 30:
            return "BUY", __min_rsi_symbol
        elif __min_rsi_value > 60:
            return "SELL", None
        else:
            return "WAIT", self.rsi.rsi_datas