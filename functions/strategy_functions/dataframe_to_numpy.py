from functions.strategy_functions.json_to_dataframe import ConverDataframe
from functions.yaml_functions.read_write import ymlReadWrite

import numpy as np


class ConvertNumpy:
    def __init__(self):
        self.dataframe = None
        self.converted = dict()

    def convert_df_to_numpyarray(self, target_column: str):
        __convert = ConverDataframe()
        __yml = ymlReadWrite()
        __convert.read_data()
        __convert.convert_js_data_to_df()
        __symbols = __yml.read_file(__yml.symbols_file)['symbols']

        for symbol in __symbols:
            values = []
            for i in range(0, len(__convert.all_converted_df_data[symbol].index)):
                index_data = __convert.all_converted_df_data[symbol][i:i + 1]
                target_value = float(index_data[target_column])
                values.append(target_value)
            __numpy_datas = np.array(values)
            self.converted[symbol] = __numpy_datas

        