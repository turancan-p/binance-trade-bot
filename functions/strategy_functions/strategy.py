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

        self.first_bool = dict()
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
            self.first_bool[symbol] = False, ""
            self.second_bool[symbol] = False, ""
            self.third_bool[symbol] = False, ""


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

        self.ema_datas.calculate_ema_datas_(50, self.data.converted)

        self.atr_datas.calculate_atr_datas_(10, self.data.converted)
        self.kelter_blue.calculate_channel_(4, self.ema_datas.ema, self.atr_datas.atr_data)
        self.kelter_red.calculate_channel_(2.75, self.ema_datas.ema, self.atr_datas.atr_data)

        self.atr_datas.calculate_atr_datas_(22, self.data.converted)
        self.my_indicator.calculate_signals_(30, self.atr_datas.atr_data, 3, self.data.converted)
        
        for symbol in self.symbols:
            symbol = f'{symbol}{self.__exchange_pair}'
            self.adx.calculate_adx_datas_(12, symbol, self.data.converted)
            __adx_value = self.adx.adx_data[symbol]
            __long_stop_value, __short_stop_value = self.my_indicator.signals[symbol]

            __last_high_value = self.all_json_data[symbol][-1][2]
            __last_low_value = self.all_json_data[symbol][-1][3]
            __last_close_value = self.all_json_data[symbol][-1][4]
            __second_last_close_value = self.all_json_data[symbol][-2][4]

            __kelter_channel_blue_up_line = self.kelter_blue.up_line[symbol]
            __kelter_channel_blue_down_line = self.kelter_blue.down_line[symbol]

            __kelter_channel_red_up_line = self.kelter_red.up_line[symbol]
            __kelter_channel_red_down_line = self.kelter_red.down_line[symbol]

            # first check kelter channel 4
            if __last_high_value > __kelter_channel_blue_up_line: # for long
                self.first_signal_wait[symbol] = 3
                self.first_bool[symbol] = True, "Long"
                self.second_bool[symbol] = False, ""
                self.second_signal_wait[symbol] = 0

            if __last_low_value < __kelter_channel_blue_down_line: # for short
                self.first_signal_wait[symbol] = 3
                self.first_bool[symbol] = True, "Short"
                self.second_bool[symbol] = False, ""
                self.second_signal_wait[symbol] = 0

            # second check kelter channel 2.75
            if self.first_bool[symbol][0] == True and self.first_signal_wait[symbol] > 0:
                if self.first_bool[symbol][1] == "Long" and __last_close_value < __kelter_channel_red_up_line:
                    self.first_signal_wait[symbol] = 0
                    self.second_bool[symbol] = True, "Long"
                    self.second_signal_wait[symbol] = 15

                elif self.first_bool[symbol][1] == "Short" and __last_close_value > __kelter_channel_red_down_line:
                    self.first_signal_wait[symbol] = 0
                    self.second_bool[symbol] = True, "Short"
                    self.second_signal_wait[symbol] = 15
                else:
                    self.first_signal_wait[symbol] = self.first_signal_wait[symbol] - 1

                if self.first_signal_wait[symbol] <= 0:
                    self.first_bool[symbol] = False, ""

            # third check adx and my own trend indicator
            if self.second_bool[symbol][0] == True and self.second_signal_wait[symbol] > 0:
                if self.second_bool[symbol][0] == "Long" and __last_close_value >= __short_stop_value and __adx_value > 40:
                    self.second_signal_wait[symbol] = 0
                    self.result_signals[symbol] = "Long"
                
                elif self.second_bool[symbol][0] == "Short" and __last_close_value <= __long_stop_value and __adx_value > 40:
                    self.second_signal_wait[symbol] = 0
                    self.result_signals[symbol] = "Short"
                else:
                    self.second_signal_wait[symbol] = self.second_signal_wait[symbol] - 1
                    self.result_signals[symbol] = f'Waiting last signal {self.second_signal_wait[symbol]}'

                if self.second_signal_wait[symbol] == 0:
                    self.second_bool[symbol] = False, ""
                    
            else:
                if self.first_bool[symbol][0] == True:
                    self.result_signals[symbol] = f'Waiting second signal {self.first_signal_wait[symbol]}'
                else:
                    self.result_signals[symbol] = f'Waiting first signal'
            
            __trend = None, __long_stop_value, __short_stop_value
            if __last_close_value >= __short_stop_value and __second_last_close_value < __short_stop_value:
                __trend = "UpTrend", __long_stop_value

            elif __last_close_value <= __long_stop_value and __second_last_close_value > __long_stop_value:
                __trend = "ShortTrend", __short_stop_value
            else:
                __trend = "ShortTrend", __long_stop_value, __short_stop_value


            __current_data_dict = {'Symbol': symbol,
             'Status': self.result_signals[symbol],
              'Last High Price': __last_high_value,
               'Last Low Price': __last_low_value,
                'Last Close Price': __last_close_value,
                'Long Stop Value': __long_stop_value,
                'Short Stop Value': __short_stop_value
                }

            __current_indicator_data_dict = {'Symbol': symbol,
                'Long Position':{
                    'Kelter x4 UpLine': __kelter_channel_blue_up_line,
                    'Kelter x2.75 UpLine': __kelter_channel_red_up_line
                    },
                'Short Position':{
                        'Kelter x4 DownLine': __kelter_channel_blue_down_line,
                        'Kelter x2.75 DownLine': __kelter_channel_red_down_line
                    },
                'Adx': __adx_value,
                'Directions': __trend
                }

            print("")
            print(__current_data_dict)
            print(__current_indicator_data_dict)
        finish_time = timeit.default_timer()
        print(f'Signal find process completed in  {finish_time - start_time} seconds')


    def find_signals(self):
        start_time = timeit.default_timer()
        self.calculate_signals()
        finish_time = timeit.default_timer()
        print(f'Signal find process completed in  {finish_time - start_time} seconds')
        return self.result_signals