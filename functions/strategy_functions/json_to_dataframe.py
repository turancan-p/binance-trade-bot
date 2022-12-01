from functions.json_functions.read_write import jsonReadWrite
from functions.yaml_functions.read_write import ymlReadWrite

import pandas as pd


class ConverDataframe():
    def __init__(self):
        self.json_reader = jsonReadWrite()
        self.yml_reader = ymlReadWrite()
        self.symbols = self.yml_reader.read_file(self.yml_reader.symbols_file)['symbols']
        self.all_json_data = None
        self.all_converted_df_data = dict()
        self.df_columns = ["Date", "Open_price", "High_price", "Low_price", "Close_price"]

    def read_data(self):
        self.all_json_data = self.json_reader.read_file(self.json_reader.all_coins_data_file)

    def convert_js_data_to_df(self):
        for symbol in self.symbols:
            self.all_converted_df_data[symbol] = pd.DataFrame(self.all_json_data[symbol], columns=self.df_columns)