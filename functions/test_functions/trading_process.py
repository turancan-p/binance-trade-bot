from functions.json_functions.read_write import jsonReadWrite
from functions.yaml_functions.read_write import ymlReadWrite

from functions.binance_functions.coin_details import CoinDetails


from functions.strategy_functions.strategy import Strategy

from datetime import datetime
from prettytable import PrettyTable
import os

class Trade():
    def __init__(self):
        self.json_functions = jsonReadWrite()
        self.yml_functions = ymlReadWrite()
        self.account_data = self.json_functions.read_file(self.json_functions.account_data_file)
        self.start_budget = self.account_data['starting_budget']
        self.symbols = self.yml_functions.read_file(self.yml_functions.symbols_file)['symbols']
        self.exchange_pair = self.yml_functions.read_file(self.yml_functions.symbols_file)['exchange_pair']
        
        self.strategy = Strategy()
        self.signals = None

        self.coin_details = None
        self.price = 0.0
        self.can_get_current_coin = True
    
    def get_signals(self):
        self.signals = self.strategy.find_signals()

    def buy_long(self, symbol, side):
        self.can_get_current_coin = True
        self.coin_details = CoinDetails(symbol)
        self.account_data = self.json_functions.read_file(self.json_functions.account_data_file)
        self.status = self.yml_functions.read_file(self.yml_functions.process_status_file)
        self.account_data['before_budget'] = self.account_data['budget']
        coin_amount, price = self.coin_details.amount_calculation(self.account_data['budget'])

        self.price = price
        
        __budget = 0.0
        __side = side
        __current_coin = symbol
        __buy_price = price
        __target_price = float(round(price + (price * 0.0075), 4))
        __stop_loss = float(round(price - (price * 0.005), 4))
        __coin_amount  = coin_amount
        __process_time = datetime.now().strftime('%d/%m/%Y %H:%M')
        __in_position = True
        __list = [__side, __current_coin, __buy_price, __target_price, __stop_loss, __coin_amount, __process_time, __in_position, __budget
]
        return __list

    def buy_short(self, symbol, side):
        self.can_get_current_coin = True
        self.coin_details = CoinDetails(symbol)
        self.account_data = self.json_functions.read_file(self.json_functions.account_data_file)
        self.status = self.yml_functions.read_file(self.yml_functions.process_status_file)
        self.account_data['before_budget'] = self.account_data['budget']
        coin_amount, price = self.coin_details.amount_calculation(self.account_data['budget'])

        self.price = price
        
        __budget = 0.0
        __side = side
        __current_coin = symbol
        __buy_price = price
        __target_price = float(round(price - (price * 0.0075), 4))
        __stop_loss = float(round(price + (price * 0.005), 4))
        __coin_amount  = coin_amount
        __process_time = datetime.now().strftime('%d/%m/%Y %H:%M')
        __in_position = True
        __list = [__side, __current_coin, __buy_price, __target_price, __stop_loss, __coin_amount, __process_time, __in_position, __budget
]
        return __list
    
    def sell(self):
        self.status = self.yml_functions.read_file(self.yml_functions.process_status_file)
        
        if self.status['side'] == 'Short':
            __budget = float(self.account_data['before_budget']+(-((self.price - self.status['buy_price']) * self.status['coin_amount'])))
        else:
            __budget = float(self.account_data['before_budget']+((self.price - self.status['buy_price']) * self.status['coin_amount']))

        __side = f'SELL - {self.status["current_coin"]}'
        __current_coin = ""
        __buy_price = ""
        __target_price = ""
        __stop_loss = ""
        __coin_amount  = 0.0
        __process_time = datetime.now().strftime('%d/%m/%Y %H:%M')
        __process_status = False

        __list = [__side, __current_coin,
         __buy_price, __target_price,
          __stop_loss, __coin_amount,
           __process_time, __process_status,
            __budget]

        return __list

    def in_position_sell_process(self):
        self.status = self.yml_functions.read_file(self.yml_functions.process_status_file)
        if self.can_get_current_coin:
            self.coin_details = CoinDetails(self.status['current_coin']) 
            self.can_get_current_coin = False

        
        self.__temp_process_side = self.status['side']

        self.process_table = PrettyTable()
        self.process_table.field_names = ['Last Process', 'Current Coin',
         'Buy Price', 'Target Price', 'Stop Price', 'Coin Amount', 
         'PNL', 'Process Time', 'In Process']
        self.account_table = PrettyTable()
        self.account_table.field_names = ['Free Budget']

        self.__temp_process_side = self.status['side']
                
        self.price = self.coin_details.get_price()
        
        if self.status['side'] == "Long" and self.price is not None:
            if self.price >= self.status['target_price'] or self.price <= self.status['stop_loss']:
                __list = self.sell()
                self.status['side'] = __list[0]
                self.status['current_coin'] = __list[1]
                self.status['buy_price'] = __list[2]
                self.status['target_price'] = __list[3]
                self.status['stop_loss'] = __list[4]
                self.status['coin_amount'] = __list[5] 
                self.status['process_time'] = __list[6] 
                self.status['in_position'] = __list[7]
                self.account_data['budget'] = __list[8]

                self.status['pnl'] = self.account_data['budget'] - self.start_budget

        elif self.status['side'] == "Short" and self.price is not None:
            if self.price <= self.status['target_price'] or self.price >= self.status['stop_loss']:
                __list = self.sell()
                self.status['side'] = __list[0]
                self.status['current_coin'] = __list[1]
                self.status['buy_price'] = __list[2]
                self.status['target_price'] = __list[3]
                self.status['stop_loss'] = __list[4]
                self.status['coin_amount'] = __list[5] 
                self.status['process_time'] = __list[6] 
                self.status['in_position'] = __list[7]
                self.account_data['budget'] = __list[8]

                self.status['pnl'] = self.account_data['budget'] - self.start_budget
                
        
        print(self.price)
        print(self.status['side'], self.__temp_process_side)
        if self.status['side'] != self.__temp_process_side:
            self.yml_functions.write_file(self.yml_functions.process_status_file, self.status)
            self.json_functions.write_file(self.json_functions.account_data_file, self.account_data)

        self.process_table.add_row([self.status['side'], self.status['current_coin'],
        self.status['buy_price'], self.status['target_price'], self.status['stop_loss'],
        self.status['coin_amount'], self.status['pnl'], self.status['process_time'],
        self.status['in_position']])

        self.account_table.add_row([self.account_data['budget']])

        print(self.account_table)
        print(self.process_table)

    
    def trade_process(self):
        self.get_signals()

        

        print("Signal Checking")
        print(self.signals)
        self.process_table = PrettyTable()
        self.process_table.field_names = ['Last Process', 'Current Coin',
         'Buy Price', 'Target Price', 'Stop Price', 'Coin Amount', 
         'PNL', 'Process Time', 'In Process']
        self.account_table = PrettyTable()
        self.account_table.field_names = ['Free Budget']

        self.status = self.yml_functions.read_file(self.yml_functions.process_status_file)
        self.account_data = self.json_functions.read_file(self.json_functions.account_data_file)
        self.__temp_process_side = self.status['side']
        
        if self.status['in_position'] == False:
            #os.system('cls')
            for symbol in self.symbols:
                symbol = f'{symbol}{self.exchange_pair}'
                if self.signals[symbol] == "Long":
                    __list = self.buy_long(symbol, "Long")
                    self.status['side'] = __list[0]
                    self.status['current_coin'] = __list[1]
                    self.status['buy_price'] = __list[2]
                    self.status['target_price'] = __list[3] 
                    self.status['stop_loss'] = __list[4]
                    self.status['coin_amount'] = __list[5] 
                    self.status['process_time'] = __list[6] 
                    self.status['in_position'] = __list[7]
                    self.account_data['budget'] = __list[8]
                
                elif self.signals[symbol] == "Short" and self.status['in_position'] == False:
                    __list = self.buy_short(symbol, "Short")
                    self.status['side'] = __list[0]
                    self.status['current_coin'] = __list[1]
                    self.status['buy_price'] = __list[2]
                    self.status['target_price'] = __list[3] 
                    self.status['stop_loss'] = __list[4]
                    self.status['coin_amount'] = __list[5] 
                    self.status['process_time'] = __list[6] 
                    self.status['in_position'] = __list[7]
                    self.account_data['budget'] = __list[8]
                


        if self.status['side'] != self.__temp_process_side:
            self.yml_functions.write_file(self.yml_functions.process_status_file, self.status)
            self.json_functions.write_file(self.json_functions.account_data_file, self.account_data)

        self.process_table.add_row([self.status['side'], self.status['current_coin'],
        self.status['buy_price'], self.status['target_price'], self.status['stop_loss'],
        self.status['coin_amount'], self.status['pnl'], self.status['process_time'],
        self.status['in_position']])

        self.account_table.add_row([self.account_data['budget']])

        print(self.account_table)
        print(self.process_table)