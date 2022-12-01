from functions.json_functions.read_write import jsonReadWrite
from functions.yaml_functions.read_write import ymlReadWrite
from functions.binance_functions.coin_details import CoinDetails
from functions.test_functions.test_strategy import TestStrategy

from datetime import datetime

import os, time

def clear_console():
    os.system('cls')

class TestTrading():
    def __init__(self):
        self.json_functions = jsonReadWrite()
        self.yml_functions = ymlReadWrite()
        
        
        self.strategy = TestStrategy()
        

    def buy(self, symbol):
        __symbol = symbol
        __coin_details = CoinDetails(__symbol)
        __account_stats = self.json_functions.read_file(self.json_functions.account_data_file)
        __coin_amount, __price = __coin_details.amount_calculation(__account_stats['budget'])
        __account_stats['budget'] = 0
        clear_console()
        print("Buying:", __symbol, "Price:", __price, "Amount:", __coin_amount)

        self.status = self.yml_functions.read_file(self.yml_functions.process_status_file)
        self.status['side'] = "BUY"
        self.status['current_coin'] = __symbol
        self.status['buy_price'] = __price
        self.status['target_price'] = float(round(__price + (__price * 0.017), 4))
        self.status['coin_amount'] = __coin_amount
        self.status['process_time'] = datetime.now()
        self.status['in_position'] = True

        self.yml_functions.write_file(self.yml_functions.process_status_file, self.status)
        self.json_functions.write_file(self.json_functions.account_data_file, __account_stats)


    def sell(self):
        self.status = self.yml_functions.read_file(self.yml_functions.process_status_file)
        __coin_details = CoinDetails(self.status['current_coin'])
        __price = __coin_details.get_price()
        __account_stats = self.json_functions.read_file(self.json_functions.account_data_file)
        clear_console()
        print("Looking sell positions for:", self.status['current_coin'])
        print("Current Price:", str(__price), "Target Price:", str(self.status['target_price']))
        if __price >= self.status['target_price']:
            __account_stats['budget'] = self.status['coin_amount'] * __coin_details.get_price()

            self.status['side'] = "SELL"
            self.status['current_coin'] = ""
            self.status['buy_price'] = 0
            self.status['target_price'] = 0
            self.status['coin_amount'] = 0
            self.status['process_time'] = datetime.now()
            self.status['in_position'] = False
        
            self.yml_functions.write_file(self.yml_functions.process_status_file, self.status)
            self.json_functions.write_file(self.json_functions.account_data_file, __account_stats)

        
    def signal(self):
        __signal, __symbol = self.strategy.strategy()
        self.status = self.yml_functions.read_file(self.yml_functions.process_status_file)
        
        if __signal == "BUY" and __symbol is not None and self.status['in_position'] == False:
            self.buy(__symbol)
        elif self.status['current_coin'] != "" and self.status['in_position'] == True:
            self.sell()
        else:
            clear_console()
            print(__symbol)
