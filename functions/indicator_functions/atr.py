import talib

from functions.yaml_functions.read_write import ymlReadWrite
from functions.strategy_functions.dataframe_to_numpy import ConvertNumpy


class AtrCalculator:
    def __init__(self):
        self.atr_datas = dict()
        self.atr_data = dict()


    
    def calculate_atr_datas(self, value: int):
        data = ConvertNumpy()
        yml = ymlReadWrite()
        symbols = yml.read_file(yml.symbols_file)['symbols']
        exchange_pair = yml.read_file(yml.symbols_file)['exchange_pair']

        __needed_columns = ['High_price', 'Low_price', 'Close_price']
        for __column in __needed_columns:
            data.convert_df_to_numpyarray(target_column=__column)

        for symbol in symbols:
            symbol = f'{symbol}{exchange_pair}'
            self.atr_datas[symbol] = talib.ATR(data.converted[f'{symbol}_High_price'], 
            data.converted[f'{symbol}_Low_price'],
            data.converted[f'{symbol}_Close_price'], value)[-1]

    def calculate_atr_datas_(self, value: int, all_numpy_data):
        yml = ymlReadWrite()
        symbols = yml.read_file(yml.symbols_file)['symbols']
        exchange_pair = yml.read_file(yml.symbols_file)['exchange_pair']

        for symbol in symbols:
            symbol = f'{symbol}{exchange_pair}'
            self.atr_data[symbol] = talib.ATR(all_numpy_data[f'{symbol}_High_price'], 
            all_numpy_data[f'{symbol}_Low_price'],
            all_numpy_data[f'{symbol}_Close_price'], value)[-1]
        