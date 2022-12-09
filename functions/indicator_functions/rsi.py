from functions.yaml_functions.read_write import ymlReadWrite
from functions.strategy_functions.dataframe_to_numpy import ConvertNumpy

import talib


class RsiCalculator:
    def __init__(self):
        self.rsi_datas = dict()

    
    def calculate_rsi_datas(self, value: int):
        data = ConvertNumpy()
        yml = ymlReadWrite()
        symbols = yml.read_file(yml.symbols_file)['symbols']
        __column_name = 'Close_price'

        data.convert_df_to_numpyarray(target_column=__column_name)
        for symbol in symbols:
            self.rsi_datas[symbol] = talib.RSI(data.converted[f'{symbol}_{__column_name}'], value)[-1]

    
    def min_rsi(self):
        min_value = min(self.rsi_datas.values())
        for key, values in self.rsi_datas.items():
            if values == min_value:
                min_symbol = str(key)
        return min_symbol, min_value
            