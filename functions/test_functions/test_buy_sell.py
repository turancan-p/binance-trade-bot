from functions.json_functions.read_write import jsonReadWrite
from functions.yaml_functions.read_write import ymlReadWrite
from functions.binance_functions.coin_details import CoinDetails

from datetime import datetime
from prettytable import PrettyTable
import os


class TestBuySell():
    def __init__(self):
        self.json_functions = jsonReadWrite()
        self.yml_functions = ymlReadWrite()
        __account_stats = self.json_functions.read_file(self.json_functions.account_data_file)
        self.start_budget = __account_stats['budget']

    def buy(self, symbol):
        __symbol = symbol
        __coin_details = CoinDetails(__symbol)
        __account_stats = self.json_functions.read_file(self.json_functions.account_data_file)
        self.status = self.yml_functions.read_file(self.yml_functions.process_status_file)
        __coin_amount, __price = __coin_details.amount_calculation(__account_stats['budget'])
        __account_stats['budget'] = 0

        self.status['side'] = "BUY"
        self.status['current_coin'] = __symbol
        self.status['buy_price'] = __price
        self.status['target_price'] = float(round(__price + (__price * 0.011), 4))
        self.status['stop_loss'] = float(round(__price - (__price * 0.022), 4))
        self.status['coin_amount'] = __coin_amount
        self.status['process_time'] = datetime.now().strftime('%d/%m/%Y %H:%M')
        self.status['in_position'] = True
        
        self.yml_functions.write_file(self.yml_functions.process_status_file, self.status)
        self.json_functions.write_file(self.json_functions.account_data_file, __account_stats)


    def sell(self):
        self.status = self.yml_functions.read_file(self.yml_functions.process_status_file)
        __account_stats = self.json_functions.read_file(self.json_functions.account_data_file)
        __coin_details = CoinDetails(self.status['current_coin'])
        self.price = __coin_details.get_price()

        if self.price >= self.status['target_price'] or self.price <= self.status['stop_loss']:
            __account_stats['budget'] = float(self.status['coin_amount'] * self.price)

            self.status['side'] = "SELL"
            self.status['current_coin'] = ""
            self.status['buy_price'] = 0
            self.status['target_price'] = 0
            self.status['stop_loss'] = 0
            self.status['coin_amount'] = 0
            self.status['pnl'] = float(__account_stats['budget'] - self.start_budget)
            self.status['process_time'] = datetime.now().strftime('%d/%m/%Y %H:%M')
            self.status['in_position'] = False
        
            self.yml_functions.write_file(self.yml_functions.process_status_file, self.status)
            self.json_functions.write_file(self.json_functions.account_data_file, __account_stats)

        
    def write_console(self):
        os.system('cls')
        __process_status_table = PrettyTable()
        __account_status_table = PrettyTable()
        self.status = self.yml_functions.read_file(self.yml_functions.process_status_file)
        __account_stats = self.json_functions.read_file(self.json_functions.account_data_file)
        __process_status_table.field_names = ['Last Process', 'Current Coin', 'Buy Price', 'Target Price',
         'Stop Price', 'Coin Amount','PNL', 'Process Time', 'In Process']
        if(self.status['in_position']):
            __current_coin_table = PrettyTable()
            __current_coin_table.field_names = ['Current Coin', 'Current Price']
            __current_coin_table.add_row([self.status["current_coin"], self.price])
            print(__current_coin_table)
        
        __process_status_table.add_row([self.status['side'], self.status['current_coin'],
        self.status['buy_price'], self.status['target_price'], self.status['stop_loss'],
        self.status['coin_amount'], self.status['pnl'], self.status['process_time'],
        self.status['in_position']])
        
        __budget = __account_stats['budget']
        __account_status_table.field_names = ['Free Budget']
        __account_status_table.add_row([__budget])
        
        print(__process_status_table)
        print(__account_status_table)