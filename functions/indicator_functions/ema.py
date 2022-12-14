import talib

from functions.yaml_functions.read_write import ymlReadWrite
from functions.strategy_functions.dataframe_to_numpy import ConvertNumpy


class EmaCalculator:
    def __init__(self):
        self.ema_datas = dict()
        self.ema = dict()


    
    def calculate_ema_datas(self, value: int):
        data = ConvertNumpy()
        yml = ymlReadWrite()
        symbols = yml.read_file(yml.symbols_file)['symbols']
        exchange_pair = yml.read_file(yml.symbols_file)['exchange_pair']
        column_name = 'Close_price'
        data.convert_df_to_numpyarray(target_column= column_name)
        for symbol in symbols:
            symbol = f'{symbol}{exchange_pair}'
            self.ema_datas[symbol] = talib.EMA(data.converted[f'{symbol}_{column_name}'], value)[-1]


    def calculate_ema_datas_(self, ema_value: int, all_numpy_data):
        yml = ymlReadWrite()
        symbols = yml.read_file(yml.symbols_file)['symbols']
        exchange_pair = yml.read_file(yml.symbols_file)['exchange_pair']
        for symbol in symbols:
            symbol = f'{symbol}{exchange_pair}'
            self.ema[symbol] = talib.EMA(all_numpy_data[f'{symbol}_Close_price'], ema_value)[-1]
    