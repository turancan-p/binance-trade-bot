# need list: high prices, low prices and atr


from functions.indicator_functions.atr import AtrCalculator
from functions.yaml_functions.read_write import ymlReadWrite
from functions.strategy_functions.dataframe_to_numpy import ConvertNumpy



class MyIndicator:
    def __init__(self):
        self.signals = dict()

    def calculate_signals(self, back_period, atr_period, atr_multiplier):
        yml = ymlReadWrite()
        atr = AtrCalculator()
        data = ConvertNumpy()

        symbols = yml.read_file(yml.symbols_file)['symbols']
        exchange_pair = yml.read_file(yml.symbols_file)['exchange_pair']

        __needed_columns = ['High_price', 'Low_price', 'Close_price']
        for __column in __needed_columns:
            data.convert_df_to_numpyarray(target_column=__column)

        atr.calculate_atr_datas(atr_period)

        for symbol in symbols:
            symbol = f'{symbol}{exchange_pair}'
            lowest = data.converted[f'{symbol}_Low_price']
            lowest_len = len(lowest)
            lowest = min(lowest[lowest_len-back_period:])

            highest = data.converted[f'{symbol}_High_price']
            highest_len = len(highest)
            highest = max(highest[highest_len-back_period:])

            last_close = data.converted[f'{symbol}_Close_price']
            last_close = last_close[-1]

            short_stop = lowest + (atr_multiplier * atr.atr_datas[symbol])
            long_stop = highest - (atr_multiplier * atr.atr_datas[symbol])


            if last_close > long_stop:
                self.signals[symbol] = "Long"# long trend
            elif last_close < short_stop:
                self.signals[symbol] = "Short"# short trend
            elif last_close == long_stop or last_close == short_stop:
                self.signals[symbol] = "Wait"# waiting for direction


    def calculate_signals_(self, back_period, atr, atr_multiplier, all_numpy_data):
            yml = ymlReadWrite()

            symbols = yml.read_file(yml.symbols_file)['symbols']
            exchange_pair = yml.read_file(yml.symbols_file)['exchange_pair']

            for symbol in symbols:
                symbol = f'{symbol}{exchange_pair}'
                lowest = all_numpy_data[f'{symbol}_Low_price']
                lowest_len = len(lowest)
                lowest = min(lowest[lowest_len-back_period:])

                highest = all_numpy_data[f'{symbol}_High_price']
                highest_len = len(highest)
                highest = max(highest[highest_len-back_period:])

                short_stop = lowest + (atr_multiplier * atr[symbol])
                long_stop = highest - (atr_multiplier * atr[symbol])


                self.signals[symbol] = long_stop, short_stop
