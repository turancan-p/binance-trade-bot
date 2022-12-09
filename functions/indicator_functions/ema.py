import talib

from functions.yaml_functions.read_write import ymlReadWrite
from functions.strategy_functions.dataframe_to_numpy import ConvertNumpy


class EmaCalculator:
    def __init__(self):
        self.ema_datas = dict()


    
    def calculate_ema_datas(self, value: int):
        data = ConvertNumpy()
        yml = ymlReadWrite()
        symbols = yml.read_file(yml.symbols_file)['symbols']
        column_name = 'Close_price'
        data.convert_df_to_numpyarray(target_column= column_name)
        for symbol in symbols:
            self.ema_datas[symbol] = talib.EMA(data.converted[f'{symbol}_{column_name}'], value)[-1]
