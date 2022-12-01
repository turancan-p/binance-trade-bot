from functions.yaml_functions.read_write import ymlReadWrite
from functions.json_functions.read_write import jsonReadWrite

from binance.client import Client
from datetime import datetime


class HistoricalData():
    def __init__(self):
        self.yml_functions = ymlReadWrite()
        self.json_functions = jsonReadWrite()

    def collect_historical_data(self):
        __api_key = self.yml_functions.read_file(self.yml_functions.client_file)['api_key']
        __api_secret = self.yml_functions.read_file(self.yml_functions.client_file)['api_secret']
        __symbols = self.yml_functions.read_file(self.yml_functions.symbols_file)['symbols']
        __interval = self.yml_functions.read_file(self.yml_functions.symbols_file)['interval']
        __limit = self.yml_functions.read_file(self.yml_functions.symbols_file)['limit']
        __new_client = Client(__api_key, __api_secret)
        __all_collected_data = dict()


        for symbol in __symbols:
            __datas = __new_client.get_historical_klines(symbol=symbol, interval=__interval, limit=__limit+1)
            __datalist = list()
            for value in __datas:
                __date = datetime.fromtimestamp(int(str(value[6])[:10])).strftime('%d/%m/%Y %H:%M')
                __open_price = float(value[1])
                __high_price = float(value[2])
                __low_price = float(value[3])
                __close_price = float(value[4])
                __new_data = [__date, __open_price, __high_price, __low_price, __close_price]
                __datalist.append(__new_data)
            print(f'Historical Data Collected: %s' % symbol)
            __datalist.pop()
            __all_collected_data[symbol] = __datalist
        self.json_functions.write_file(self.json_functions.all_coins_data_file,__all_collected_data)
