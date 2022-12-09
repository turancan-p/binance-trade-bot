import talib

from functions.indicator_functions.ema import EmaCalculator
from functions.indicator_functions.atr import AtrCalculator
from functions.yaml_functions.read_write import ymlReadWrite


class KeltnerChannel:
    def __init__(self):
        self.middle_line = dict()
        self.up_line = dict()
        self.down_line = dict()

    def calculate_channel(self, atr_multiplier):
        yml = ymlReadWrite()
        ema_50 = EmaCalculator()
        atr_50 = AtrCalculator()

        ema_50.calculate_ema_datas(50)  
        atr_50.calculate_atr_datas(10)

        symbols = yml.read_file(yml.symbols_file)['symbols']
        for symbol in symbols:
            self.middle_line[symbol] = ema_50.ema_datas[symbol]
            self.up_line[symbol] = ema_50.ema_datas[symbol]  + (atr_50.atr_datas[symbol] * atr_multiplier)
            self.down_line[symbol] = ema_50.ema_datas[symbol]  - (atr_50.atr_datas[symbol] * atr_multiplier)