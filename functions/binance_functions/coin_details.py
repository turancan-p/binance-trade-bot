from functions.yaml_functions.read_write import ymlReadWrite

from binance.client import Client
from decimal import Decimal

import requests



class CoinDetails:
    def __init__(self, symbol):
        __yml_functions = ymlReadWrite()
        __api_key = __yml_functions.read_file(__yml_functions.client_file)['api_key']
        __api_secret = __yml_functions.read_file(__yml_functions.client_file)['api_secret']
        
        self.symbol = symbol
        self.client = Client(__api_key, __api_secret)
        
    def get_price(self):
        __url = f'https://api.binance.com/api/v3/ticker/price?symbol={self.symbol}'
        __response = requests.get(__url)
        __response = __response.json()
        __price = float(__response['price'])
        return __price

    def get_tick_size(self):
        __coin_info = self.client.get_symbol_info(self.symbol)
        __tick_size = __coin_info["filters"][0]["tickSize"]
        return __tick_size
    
    def amount_calculation(self, budget):
        __budget = budget
        __tick_size = self.get_tick_size()
        __price = self.get_price()
        __quantity = __budget / __price
        __quantity = Decimal(str(__quantity))
        __rounded_quantity = float(__quantity - __quantity % Decimal(str(__tick_size)))
        return __rounded_quantity, __price