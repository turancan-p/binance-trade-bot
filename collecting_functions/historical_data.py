from datetime import datetime
from binance_functions.client_functions.binance_client import CreateClient
from decouple import config
from settings.bot_settings import *
from multiprocessing import Pool

import timeit
import json

class HistoricalData:
    def __init__(self):
        if config('API_KEY') != None and config('SECRET_KEY') != None:
            self.api_key = config('API_KEY')
            self.secret_key = config('SECRET_KEY')
        else:
            self.api_key = ""
            self.secret_key = ""
        self.symbol_list = SYMBOL_LIST
        self.exchange_pair = EXCHANGE_PAIR
        self.interval = INTERVAL
        self.all_data = dict()
        self.my_client = CreateClient(self.api_key, self.secret_key).client()

    def historical(self, symbol):
        all_datas = self.my_client.get_historical_klines(symbol=symbol+self.exchange_pair, interval=self.interval, limit=1000)
        converted_datas = list()
        data_dict = dict()
        for value in all_datas:
            __date = datetime.fromtimestamp(int(str(value[6])[:10]))
            __date = __date.strftime('%d/%m/%Y %H:%M')
            __open_price = float(value[1])
            __high_price = float(value[2])
            __low_price = float(value[3])
            __close_price = float(value[4])
            __new_data = [__date, __open_price, __high_price, __low_price, __close_price]
            converted_datas.append(__new_data)
        converted_datas.pop()
        data_dict[symbol+self.exchange_pair] = converted_datas
        return data_dict


    def collect_historical(self):
        historical_process_start_time = timeit.default_timer()
        p = Pool()
        result = p.map(self.historical, self.symbol_list)

        p.close()
        p.join()

        historical_process_finish_time = timeit.default_timer()
        for data in result:
            self.all_data[list(data.keys())[0]] = list(data.values())[0]
        with open("./data/all_data.json", 'w') as file:
            json.dump(self.all_data, file)
        
        print("Collect Historical Data Process Take:",historical_process_finish_time - historical_process_start_time, "Seconds")
        return True