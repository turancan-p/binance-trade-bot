import talib

from functions.yaml_functions.read_write import ymlReadWrite
from functions.strategy_functions.dataframe_to_numpy import ConvertNumpy


class AdxCalculator:
    def __init__(self):
        self.atr_data = None
        self.adx_data = dict()


    
    def calculate_adx_datas(self, value: int, symbol: str):
        data = ConvertNumpy()
        __needed_columns = ['High_price', 'Low_price', 'Close_price']
        for __column in __needed_columns:
            data.convert_df_to_numpyarray(target_column=__column)

        self.atr_data = talib.ADX(data.converted[f'{symbol}_High_price'], 
        data.converted[f'{symbol}_Low_price'],
        data.converted[f'{symbol}_Close_price'], value)[-1]
        
    def calculate_adx_datas_(self, value: int, symbol: str, all_numpy_data):
        self.adx_data[symbol] = talib.ADX(all_numpy_data[f'{symbol}_High_price'], 
        all_numpy_data[f'{symbol}_Low_price'],
        all_numpy_data[f'{symbol}_Close_price'], value)[-1]