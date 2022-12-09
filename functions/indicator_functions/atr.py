import talib

from functions.yaml_functions.read_write import ymlReadWrite
from functions.strategy_functions.dataframe_to_numpy import ConvertNumpy


class AtrCalculator:
    def __init__(self):
        self.atr_datas = dict()


    
    def calculate_atr_datas(self, value: int):
        data = ConvertNumpy()
        yml = ymlReadWrite()
        symbols = yml.read_file(yml.symbols_file)['symbols']
        __needed_columns = ['High_price', 'Low_price', 'Close_price']
        for __column in __needed_columns:
            data.convert_df_to_numpyarray(target_column=__column)

        for symbol in symbols:
            self.atr_datas[symbol] = talib.ATR(data.converted[f'{symbol}_High_price'], 
            data.converted[f'{symbol}_Low_price'],
            data.converted[f'{symbol}_Close_price'], value)[-1]
        