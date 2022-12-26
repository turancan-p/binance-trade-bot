from indicator_functions.ema import EmaCalculator 
from indicator_functions.adx import AdxCalculator
from indicator_functions.atr import AtrCalculator
from indicator_functions.trend_find import TrendFinder
from indicator_functions.keltner_channel import KeltnerChannel
from convert_functions.convert_numpy import NumpyConventer

from settings.bot_settings import *

import yaml
import timeit

class Strategy:
    def __init__(self):
        self.last_high_value = dict()
        self.last_low_value = dict()
        self.last_close_value = dict()
        self.second_last_close_value = dict()
        self.first_check = dict()
        self.second_check = dict()
        self.third_check = dict()
        self.symbols = SYMBOL_LIST
        self.exchange_pair = EXCHANGE_PAIR

        for symbol in self.symbols:
            symbol = symbol + self.exchange_pair

            self.first_check[symbol] = [False, "", 0]
            self.second_check[symbol] = [False, "", 0]
            self.third_check[symbol] = [""]

    def find_signal(self):
        start_time = timeit.default_timer()
                    
        all_numpy_data, all_keys = NumpyConventer().convert()

        ema_calculator_50 = EmaCalculator()
        adx_calculator_12 = AdxCalculator()
        atr_calculator_10 = AtrCalculator()
        atr_calculator_22 = AtrCalculator()
        trend_finder = TrendFinder()
        keltner_channel_blue = KeltnerChannel()
        keltner_channel_red = KeltnerChannel()

        for symbol in self.symbols:
            symbol = symbol + self.exchange_pair
            self.last_high_value[symbol] = all_numpy_data[f'{symbol}_high_price'][-1]
            self.last_low_value[symbol] = all_numpy_data[f'{symbol}_low_price'][-1]
            self.last_close_value[symbol] = all_numpy_data[f'{symbol}_close_price'][-1]
            self.second_last_close_value[symbol] = all_numpy_data[f'{symbol}_close_price'][-2]

            ema_calculator_50.calculate(symbol, all_numpy_data[f'{symbol}_close_price'],50)
            adx_calculator_12.calculate(symbol, all_numpy_data[f'{symbol}_high_price'], all_numpy_data[f'{symbol}_low_price'], all_numpy_data[f'{symbol}_close_price'])
            atr_calculator_10.calculate(symbol, all_numpy_data[f'{symbol}_high_price'], all_numpy_data[f'{symbol}_low_price'], all_numpy_data[f'{symbol}_close_price'], 10)
            atr_calculator_22.calculate(symbol, all_numpy_data[f'{symbol}_high_price'], all_numpy_data[f'{symbol}_low_price'], all_numpy_data[f'{symbol}_close_price'], 22)
            keltner_channel_blue.calculate(symbol, atr_calculator_10.atr_datas[symbol], ema_calculator_50.ema_datas[symbol], 4)
            keltner_channel_red.calculate(symbol, atr_calculator_10.atr_datas[symbol], ema_calculator_50.ema_datas[symbol], 2.75)
            trend_finder.calculate(symbol, atr_calculator_22.atr_datas[symbol], 3, all_numpy_data[f'{symbol}_high_price'], all_numpy_data[f'{symbol}_low_price'], 22)

        
            # first check
            # if last high price is higher then keltner blue up line = send short signal
            # if last low price is lower then keltner blue down line = send long signal
            if self.last_high_value[symbol] > keltner_channel_blue.up_line[symbol]:
                self.first_check[symbol] = [True, "Short", 3]
            elif self.last_low_value[symbol] < keltner_channel_blue.down_line[symbol]:
                self.first_check[symbol] = [True, "Long", 3]
            # second check
            # if last close price is lower then keltner red up line = send short signal
            # if last close price is higher then keltner red down line = send long signal
        
            if self.first_check[symbol][0] == True:                    
                if self.first_check[symbol][1] == "Short" and self.last_close_value[symbol] < keltner_channel_red.up_line[symbol] and self.first_check[symbol][2] > 0:
                    self.second_check[symbol] = [True, "Short", 15]
                    self.first_check[symbol] = [False, "", 0]
                elif self.first_check[symbol][1] == "Long" and self.last_close_value[symbol] > keltner_channel_red.down_line[symbol] and self.first_check[symbol][2] > 0:
                    self.second_check[symbol] = [True, "Long", 15]
                    self.first_check[symbol] = [False, "", 0]
                    
                self.first_check[symbol][2] = self.first_check[symbol][2] - 1
                if self.first_check[symbol][2] <= 0:
                    self.first_check[symbol] = [False, "", 0]
            # third check
            # check trend is long or short then check adx > 30 = send third signal
        
            if self.second_check[symbol][0] == True:
                if self.second_check[symbol][1] == "Short" and self.second_check[symbol][2] > 0 and self.last_close_value[symbol] < trend_finder.trend[symbol]["trend_line"] and adx_calculator_12.adx_datas[symbol] > 30:
                    self.third_check[symbol] = ["Short"]
                    self.second_check[symbol] = [False, "", 0]
                elif self.second_check[symbol][1] == "Long" and self.second_check[symbol][2] > 0 and self.last_close_value[symbol] > trend_finder.trend[symbol]["trend_line"] and adx_calculator_12.adx_datas[symbol] > 30:
                    self.third_check[symbol] = ["Long"]
                    self.second_check[symbol] = [False, "", 0]
                self.second_check[symbol][2] = self.second_check[symbol][2] - 1
                if self.second_check[symbol][2] <= 0:
                    self.second_check[symbol] = [False, "", 0]                
            print("")
            print(symbol, self.first_check[symbol], self.second_check[symbol], self.third_check[symbol])         
        print("")
        finish_time = timeit.default_timer()
        print(f'Signal checking finished {finish_time - start_time} seconds')
        print("")
