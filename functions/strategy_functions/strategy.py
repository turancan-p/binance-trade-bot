from functions.indicator_functions.keltner_channel import KeltnerChannel
from functions.indicator_functions.my_indicator import MyIndicator
from functions.indicator_functions.adx import AdxCalculator
from functions.yaml_functions.read_write import ymlReadWrite
from functions.json_functions.read_write import jsonReadWrite

from functions.strategy_functions.dataframe_to_numpy import ConvertNumpy
from functions.indicator_functions.ema import EmaCalculator
from functions.indicator_functions.atr import AtrCalculator



import timeit


class Strategy:
    def __init__(self):
        self.__yml = ymlReadWrite()
        self.symbols = self.__yml.read_file(self.__yml.symbols_file)['symbols']
        self.__exchange_pair = self.__yml.read_file(self.__yml.symbols_file)['exchange_pair']
        self.data = ConvertNumpy()
        self.kelter_blue = KeltnerChannel()
        self.kelter_red = KeltnerChannel()
        self.ema_datas = EmaCalculator()
        self.atr_datas = AtrCalculator()
        self.my_indicator = MyIndicator()
        self.adx = AdxCalculator()

        self.fisrt_bool = dict()
        self.second_bool = dict()
        self.third_bool = dict()

        self.json_reader = jsonReadWrite()
        self.all_json_data = self.json_reader.read_file(self.json_reader.all_coins_data_file)

        self.result_signals = dict()
        self.first_signal_wait = dict()
        self.second_signal_wait = dict()
        self.third_signal_wait = dict()
        self.last_signal_wait = dict()


        for symbol in self.symbols:
            symbol = f'{symbol}{self.__exchange_pair}'
            self.first_signal_wait[symbol] = 0
            self.second_signal_wait[symbol] = 0
            self.third_signal_wait[symbol] = 0
            self.last_signal_wait[symbol] = 0
            self.fisrt_bool[symbol] = False
            self.second_bool[symbol] = False
            self.third_bool[symbol] = False


        self.calculate_signals()


    def calculate_signals(self):
        print("data read process starting")
        start_time = timeit.default_timer()
        
        self.all_json_data = self.json_reader.read_file(self.json_reader.all_coins_data_file)
        
        finish_time = timeit.default_timer()
        print(f'all data read process completed in  {finish_time - start_time} seconds')

        print("")
        print("data convert process starting")
        start_time = timeit.default_timer()

        __column_name = 'Open_price', 'High_price', 'Low_price', 'Close_price'
        for __column in __column_name:
            self.data.convert_df_to_numpyarray(target_column=__column)

        finish_time = timeit.default_timer()

        print(f'data convert process completed in  {finish_time - start_time} seconds')
        
        print("")
        print("signal find process starting")
        start_time = timeit.default_timer()

        self.ema_datas.calculate_ema_datas_(20, self.data.converted)
        self.atr_datas.calculate_atr_datas_(10, self.data.converted)
        self.kelter_blue.calculate_channel_(4, self.ema_datas.ema, self.atr_datas.atr_data)
        self.kelter_red.calculate_channel_(2.75, self.ema_datas.ema, self.atr_datas.atr_data)

        self.atr_datas.calculate_atr_datas_(22, self.data.converted)
        self.my_indicator.calculate_signals_(30, self.atr_datas.atr_data, 3, self.data.converted)
        
        for symbol in self.symbols:
            symbol = f'{symbol}{self.__exchange_pair}'

            if self.all_json_data[symbol][-1][2] > self.kelter_blue.up_line[symbol]:
                self.result_signals[symbol] = {"Signal": "First Short Signal", "Wait Period": self.second_signal_wait[symbol]}
                self.second_signal_wait[symbol] = 3
                self.second_bool[symbol] = True
            elif self.all_json_data[symbol][-1][3] < self.kelter_blue.down_line[symbol]: 
                self.result_signals[symbol] = {"Signal": "First Long Signal", "Wait Period": self.second_signal_wait[symbol]}
                self.second_signal_wait[symbol] = 3
                self.second_bool[symbol] = True
            else:
                self.result_signals[symbol] = {"Signal": "Waiting First Signal", "Wait Period": self.second_signal_wait[symbol]}
            
            if self.second_bool[symbol] == True:
                if self.second_signal_wait[symbol] > 0 and self.all_json_data[symbol][-1][4] < self.kelter_red.up_line[symbol]:
                        self.result_signals[symbol] = {"Signal": "Second Short Signal", "Wait Period": self.second_signal_wait[symbol]}
                        self.third_signal_wait[symbol] = 15
                        self.third_bool[symbol] = True

                elif self.second_signal_wait[symbol] > 0 and self.all_json_data[symbol][-1][4] > self.kelter_red.down_line[symbol]:
                        self.result_signals[symbol] = {"Signal": "Second Long Signal", "Wait Period": self.second_signal_wait[symbol]}
                        self.third_signal_wait[symbol] = 15
                        self.third_bool[symbol] = True

                else:
                    self.result_signals[symbol] = {"Signal": "Waiting Second Signal", "Wait Period": self.second_signal_wait[symbol]}
                
                if self.second_signal_wait[symbol] > 0:
                    self.second_signal_wait[symbol] = self.second_signal_wait[symbol] - 1
                else:
                    self.second_bool[symbol] = False

            
            if self.third_signal_wait[symbol] > 0 and self.third_bool[symbol] == True:
                self.adx.calculate_adx_datas_(12, symbol, self.data.converted)
                if self.my_indicator.signals[symbol][0] > self.all_json_data[symbol][-1][4] and self.adx.adx_data[symbol] > 40:
                    self.result_signals[symbol] = {"Signal": "Last Long Signal", "Wait Period": self.third_signal_wait[symbol]}

                elif self.my_indicator.signals[symbol][1] < self.all_json_data[symbol][-1][4] and self.adx.adx_data[symbol] > 40:
                    self.result_signals[symbol] = {"Signal": "Last Short Signal", "Wait Period": self.third_signal_wait[symbol]}
                else:
                    self.result_signals[symbol] = {"Signal": "Waiting Last Signal", "Wait Period": self.third_signal_wait[symbol]}
                if self.third_signal_wait[symbol] > 0:
                    self.third_signal_wait[symbol] = self.third_signal_wait[symbol] - 1
                else:
                    self.third_bool[symbol] = False

            print(symbol)
            print(self.result_signals[symbol])
            print(f'Long stop: {self.my_indicator.signals[symbol][0]} Short stop: {self.my_indicator.signals[symbol][1]}')
        finish_time = timeit.default_timer()
        print(f'Signal find process completed in  {finish_time - start_time} seconds')


    def find_signals(self):
        start_time = timeit.default_timer()
        self.calculate_signals()
        finish_time = timeit.default_timer()
        print(f'Signal find process completed in  {finish_time - start_time} seconds')
        return self.result_signals