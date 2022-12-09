from functions.json_functions.read_write import jsonReadWrite
from functions.yaml_functions.read_write import ymlReadWrite

from functions.binance_functions.coin_details import CoinDetails


from functions.indicator_functions.rsi import RsiCalculator

from datetime import datetime
from prettytable import PrettyTable
import os

class Trade():
    def __init__(self):
        self.json_functions = jsonReadWrite()
        self.yml_functions = ymlReadWrite()
        self.account_data = self.json_functions.read_file(self.json_functions.account_data_file)
        self.start_budget = self.account_data['budget']
        
        self.rsi = RsiCalculator()

        self.coin_details = None
        self.price = 0.0
    
    def get_signals(self):
        self.rsi.calculate_rsi_datas(20)
        __min_rsi_symbol, __min_rsi_value = self.rsi.min_rsi()
        if __min_rsi_value < 25:
            return "BUY", __min_rsi_symbol
        else:
            return "WAIT", self.rsi.rsi_datas

    def buy(self, symbol):
        self.coin_details = CoinDetails(symbol)
        self.account_data = self.json_functions.read_file(self.json_functions.account_data_file)
        self.status = self.yml_functions.read_file(self.yml_functions.process_status_file)

        coin_amount, price = self.coin_details.amount_calculation(self.account_data['budget'])

        self.price = price
        
        __budget = 0.0
        __side = "BUY"
        __current_coin = symbol
        __buy_price = price
        __target_price = float(round(price + (price * 0.01), 4))
        __stop_loss = float(round(price - (price * 0.03), 4))
        __coin_amount  = coin_amount
        __process_time = datetime.now().strftime('%d/%m/%Y %H:%M')
        __in_position = True

        return __side, __current_coin, __buy_price, __target_price, __stop_loss, __coin_amount, __process_time, __in_position, __budget

    
    def sell(self):
        self.status = self.yml_functions.read_file(self.yml_functions.process_status_file)
        self.coin_details = CoinDetails(self.status['current_coin'])
        self.price = self.coin_details.get_price()
        
        if self.price >= self.status['target_price'] or self.price <= self.status['stop_loss']:
            __budget = float(self.status['coin_amount'] * self.price)
            __side = "SELL"
            __current_coin = ""
            __buy_price = ""
            __target_price = ""
            __stop_loss = ""
            __coin_amount  = 0.0
            __process_time = datetime.now().strftime('%d/%m/%Y %H:%M')
            __process_status = False

        return __side, __current_coin, __buy_price, __target_price, __stop_loss, __coin_amount, __process_time, __process_status, __budget

    
    def trade_process(self):
        os.system('cls')
        self.process_table = PrettyTable()
        self.process_table.field_names = ['Last Process', 'Current Coin',
         'Buy Price', 'Target Price', 'Stop Price', 'Coin Amount', 
         'PNL', 'Process Time', 'In Process']
        self.account_table = PrettyTable()
        self.account_table.field_names = ['Free Budget']

        self.status = self.yml_functions.read_file(self.yml_functions.process_status_file)
        self.account_data = self.json_functions.read_file(self.json_functions.account_data_file)
        __temp_process_side = self.status['side']

        if self.get_signals() == "BUY":
            self.status['side'], self.status['current_coin'], self.status['buy_price'], 
            self.status['target_price'], self.status['stop_loss'], self.status['coin_amount'], 
            self.status['process_time'],self.status['in_position'], self.account_data['budget'] = self.buy()

        elif self.get_signals() == "SELL":
            self.status['side'], self.status['current_coin'], self.status['buy_price'], 
            self.status['target_price'], self.status['stop_loss'], self.status['coin_amount'], 
            self.status['process_time'],self.status['in_position'], self.account_data['budget'] = self.sell()

        elif self.status['side'] != __temp_process_side:
            self.yml_functions.write_file(self.yml_functions.process_status_file, self.status)
            self.json_functions.write_file(self.json_functions.account_data_file, self.account_data)

        self.process_table.add_row([self.status['side'], self.status['current_coin'],
        self.status['buy_price'], self.status['target_price'], self.status['stop_loss'],
        self.status['coin_amount'], self.status['pnl'], self.status['process_time'],
        self.status['in_position']])

        self.account_table.add_row([self.account_data['budget']])

        print(self.account_table)
        print(self.account_table)