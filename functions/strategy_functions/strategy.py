from functions.indicator_functions.keltner_channel import KeltnerChannel
from functions.indicator_functions.adx import AdxCalculator
from functions.yaml_functions.read_write import ymlReadWrite
from functions.json_functions.read_write import jsonReadWrite

import timeit


class Strategy:
    def __init__(self):
        __yml = ymlReadWrite()
        self.symbols = __yml.read_file(__yml.symbols_file)['symbols']
        self.kelter_blue = KeltnerChannel()
        self.kelter_red = KeltnerChannel()
        self.adx = AdxCalculator()
        self.json_reader = jsonReadWrite()
        self.all_json_data = self.json_reader.read_file(self.json_reader.all_coins_data_file)
        self.first_signals = dict()
        self.second_signals = dict()
        self.third_signals = dict()
        self.result_signals = dict()
        self.max_wait = dict()
        for symbol in self.symbols:
            self.max_wait[symbol] = 0


    def first_signal(self):
        self.all_json_data = self.json_reader.read_file(self.json_reader.all_coins_data_file)
        self.kelter_blue.calculate_channel(4)       
        for symbol in self.symbols:
            #print(symbol)
            #print(f'blue_upline: {self.kelter_blue.up_line[symbol]}')
            #print(f'blue_downline: {self.kelter_blue.down_line[symbol]}')
            if self.all_json_data[symbol][-1][2] > self.kelter_blue.up_line[symbol]:
                self.first_signals[symbol] = "Short"
                self.max_wait[symbol] = 10
            elif self.all_json_data[symbol][-1][3] < self.kelter_blue.down_line[symbol]: 
                self.first_signals[symbol] = "Long"
                self.max_wait[symbol] = 10
            elif self.max_wait[symbol] == 0:
                self.first_signals[symbol] = "Waiting for first signal"
        print("first signals")
        print(self.first_signals)

    def second_signal(self):
        self.first_signal()
        self.kelter_red.calculate_channel(2.75)
        for symbol in self.symbols:
            #print(symbol)
            #print(f'red_upline: {self.kelter_red.up_line[symbol]}')
            #print(f'red_downline: {self.kelter_red.down_line[symbol]}')
            if self.first_signals[symbol] != "Waiting for first signal" and self.max_wait[symbol] > 0:

                if self.first_signals[symbol] == "Short" and self.all_json_data[symbol][-1][4] < self.kelter_red.up_line[symbol]:
                    self.second_signals[symbol] = "Short"
                
                elif self.first_signals[symbol] == "Long" and self.all_json_data[symbol][-1][4] > self.kelter_red.down_line[symbol]: 
                    self.second_signals[symbol] = "Long"
                
                else:
                    self.second_signals[symbol] = f'Waiting for second signal last: {self.max_wait[symbol]} times'
            else:
                self.second_signals[symbol] = self.first_signals[symbol]
            
            if self.max_wait[symbol] > 0:
                self.max_wait[symbol] = self.max_wait[symbol] - 1
        
        print("second signals")
        print(self.second_signals)
        print("Max wait")
        print(self.max_wait)

        
    def third_signal(self):
        self.second_signal()
        for symbol in self.symbols:
            if self.second_signals[symbol] == "Short" or self.second_signals[symbol] == "Long":
                self.adx.calculate_adx_datas(12, symbol)
                print(symbol, self.adx.atr_data)
                if self.adx.atr_data > 40 and self.adx.atr_data < 50 and self.second_signals[symbol] == "Short":
                    self.third_signals[symbol] = "Short"
                elif self.adx.atr_data > 40 and self.adx.atr_data < 50 and self.second_signals[symbol] == "Long":
                    self.third_signals[symbol] = "Long"
                else:
                    self.third_signals[symbol] = "Wait"
                    self.max_wait[symbol] = 0
            else:
                self.third_signals[symbol] = "Wait"

    def find_signals(self):
        start_time = timeit.default_timer()
        self.third_signal()
        self.result_signals = self.third_signals
        finish_time = timeit.default_timer()
        print(f'Signal find process completed in  {finish_time - start_time} seconds')
        return self.result_signals