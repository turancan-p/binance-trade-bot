from json import JSONEncoder
from settings.bot_settings import *

import json
import numpy
import timeit


class NumpyConventer(JSONEncoder):
    def convert(self):
        program_start_time = timeit.default_timer()

        __symbols = SYMBOL_LIST
        __exchange_pair = EXCHANGE_PAIR
        __target_columns = ["_open_price", "_high_price", "_low_price", "_close_price"]

        __all_json_data = dict()
        __all_list_data = dict()
        __numpy_datas = dict()

        for symbol in __symbols:
            symbol = symbol + __exchange_pair
            for column in __target_columns:
                __all_list_data[symbol+column] = list()

        with open("./data/all_data.json", "r") as file:
            __all_json_data = json.load(file)

        for symbol in __symbols:
            symbol = symbol + __exchange_pair
            for x in range(0, len(__all_json_data[symbol])):
                for i, column in enumerate(__target_columns):
                    __all_list_data[symbol+column].append(__all_json_data[symbol][x][i+1])
            
        for key in __all_list_data.keys():
            __numpy_datas[key] = numpy.array(__all_list_data[key])

        program_process_finish_time = timeit.default_timer()
        print("Convert Process Take:",program_process_finish_time - program_start_time, "Seconds")
        return __numpy_datas, list(__all_list_data.keys())