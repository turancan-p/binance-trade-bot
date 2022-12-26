from binance_functions.client_functions.binance_client import CreateClient

from decouple import config
from decimal import Decimal
from requests.exceptions import Timeout

import requests
import time

class CoinDetails:
    def __init__(self):
        if config('API_KEY') != None and config('SECRET_KEY') != None:
            self.api_key = config('API_KEY')
            self.secret_key = config('SECRET_KEY')
        else:
            self.api_key = ""
            self.secret_key = ""
        
        self.my_client = CreateClient(self.api_key, self.secret_key).client()

    def get_tick_size(self, symbol):
        __coin_info = self.my_client.get_symbol_info(symbol)
        __tick_size = __coin_info["filters"][0]["tickSize"]
        return __tick_size
    
    def get_price(self, symbol: str):
        try:
            time.sleep(0.5)
            __url = f'https://api.binance.com/api/v3/ticker/price?symbol={symbol.upper()}'
            __response = requests.get(__url, timeout=1)

            __response = __response.json()
            __price = float(__response['price'])
            return __price
        except Timeout as to:
            return None

    def amount_calculation(self, symbol, budget, price = None):
        __budget = budget
        __tick_size = self.get_tick_size(symbol)
        if price == None:
            __price = self.get_price(symbol)
            while __price == None:
                __price = self.get_price(symbol)
        else:
            __price = float(price)
            
        __quantity = __budget / __price
        __quantity = Decimal(str(__quantity))
        __rounded_quantity = float(__quantity - __quantity % Decimal(str(__tick_size)))
        return __rounded_quantity