from binance_functions.coin_functions.coin_details import CoinDetails
from strategy_functions.strategy import Strategy

from settings.bot_settings import SYMBOL_LIST, EXCHANGE_PAIR

from prettytable import PrettyTable
from datetime import datetime

import json
import yaml

class Trade():
    def __init__(self):
        self.strategy = Strategy()
        self.coin_details = CoinDetails()

        self.symbols = SYMBOL_LIST
        self.exchange = EXCHANGE_PAIR

        with open("./test_process/account_stats.yml", "r") as account_file:
            self.account_stats = yaml.load(account_file, Loader=yaml.FullLoader)
        with open("./test_process/process_status.json", "r") as process_file:
            self.process_status = json.load(process_file)

        self.process_list = []
        for process in self.process_status.keys():
            self.process_list.append(process)


    def check_signals(self):
        while True:
            with open("./settings/controller.yml", "r") as file:
                __controller = yaml.load(file, Loader=yaml.FullLoader)
            
            with open("./test_process/process_status.json", "r") as process_file:
                __process_status = json.load(process_file)
            
            if __controller != None:
                if __controller["can_check_signals"] == True:
                    self.strategy.find_signal()
                    __controller["can_check_signals"] = False

                    with open("./settings/controller.yml", "w") as file:
                        yaml.safe_dump(__controller, file)

                    for process in self.process_list:
                        if __process_status[process]["in_position"] == False:
                            self.buy(process)
                            
            for process in self.process_list:
                if __process_status[process]["in_position"] == True:               
                    self.sell(process)
            
            for __symbol in self.symbols:
                __symbol = __symbol + self.exchange
                self.strategy.third_check[__symbol][0] = ""
                    
                             
    def buy(self, process):
        with open("./test_process/account_stats.yml", "r") as account_file:
            __account_stats = yaml.load(account_file, Loader=yaml.FullLoader)
        with open("./test_process/process_status.json", "r") as process_file:
            __process_status = json.load(process_file)

        if __account_stats['money'] > 100:
            __used_money = 100
        else:
            __used_money = __account_stats['money']

        for __symbol in self.symbols:
            __symbol = __symbol + self.exchange
            if self.strategy.third_check[__symbol][0] == "Long" or self.strategy.third_check[__symbol][0] == "Short":
                __process_time = datetime.now().strftime('%d/%m/%Y %H:%M')
                __current_coin = __symbol
                __process_start_price = self.coin_details.get_price(__symbol)
                while __process_start_price == None:
                    __process_start_price = self.coin_details.get_price(__symbol)
                    
                __coin_amount = self.coin_details.amount_calculation(__symbol, __used_money, __process_start_price)
                __in_position = True
                if self.strategy.third_check[__symbol][0] == "Long":
                    __last_process = "Long"
                    __take_profit_price = float(round(__process_start_price + (__process_start_price * 0.0075), 4))
                    __stop_loss_price = float(round(__process_start_price - (__process_start_price * 0.005), 4))
                if self.strategy.third_check[__symbol][0] == "Short":
                    __last_process = "Short"
                    __take_profit_price = float(round(__process_start_price - (__process_start_price * 0.0075), 4))
                    __stop_loss_price = float(round(__process_start_price + (__process_start_price * 0.005), 4))
                
                

                __process_status[process]["last_process"] = __last_process
                __process_status[process]["process_time"] = __process_time
                __process_status[process]["current_coin"] = __current_coin
                __process_status[process]["coin_amount"] = __coin_amount
                __process_status[process]["process_start_price"] = __process_start_price
                __process_status[process]["take_profit_price"] = __take_profit_price
                __process_status[process]["stop_loss_price"] = __stop_loss_price
                __process_status[process]["in_position"] = __in_position
                __process_status[process]['used_money'] = __used_money

                __account_stats['money'] = __account_stats['money'] - __used_money
                with open("./test_process/process_status.json", "w") as process_file:
                    json.dump(__process_status, process_file)

                with open("./test_process/account_stats.yml", "w") as account_stats_file:
                    yaml.safe_dump(__account_stats, account_stats_file)
                print(__symbol, "breaking")
                break

    def sell(self, process):
        __can_trade = False
        __pnl = 0.0
        with open("./test_process/process_status.json", "r") as process_file:
            __process_status = json.load(process_file)

        __last_process = __process_status[process]["last_process"]
        __current_coin = __process_status[process]["current_coin"]
        __current_price = self.coin_details.get_price(__current_coin)
        while __current_price == None:
            __current_price = self.coin_details.get_price(__current_coin)
        __take_profit_price = __process_status[process]["take_profit_price"]
        __stop_loss_price = __process_status[process]["stop_loss_price"]
        __process_start_price = __process_status[process]["process_start_price"]
        __coin_amount = __process_status[process]["coin_amount"]


        if __last_process == "Long":
            if __current_price <= __stop_loss_price or __current_price >= __take_profit_price:
                __can_trade = True
                __pnl = round(float((__current_price - __process_start_price) * __coin_amount), 2)
        if __last_process == "Short":
            if __current_price >= __stop_loss_price or __current_price <= __take_profit_price:
                __can_trade = True
                __pnl = -(round(float((__current_price - __process_start_price) * __coin_amount), 2))

        if __can_trade:
            with open("./test_process/account_stats.yml", "r") as account_file:
                __account_stats = yaml.load(account_file, Loader=yaml.FullLoader)

            __account_stats['money'] = __process_status[process]['used_money'] + __pnl
            __account_stats['pnl'] = __account_stats['pnl'] + __pnl
            
            __last_process = f'SELL - {self.process_status[process]["current_coin"]}'
            __current_coin = None
            __buy_price = None
            __target_price = None
            __stop_loss = None
            __coin_amount  = None
            __process_time = datetime.now().strftime('%d/%m/%Y %H:%M')
            __in_position = False

            __process_status[process]["last_process"] = __last_process
            __process_status[process]["process_time"] = __process_time
            __process_status[process]["current_coin"] = __current_coin
            __process_status[process]["coin_amount"] = __coin_amount
            __process_status[process]["process_start_price"] = __buy_price
            __process_status[process]["take_profit_price"] = __target_price
            __process_status[process]["stop_loss_price"] = __stop_loss
            __process_status[process]["in_position"] = __in_position
            __process_status[process]['used_money'] = 0.0

            with open("./test_process/process_status.json", "w") as process_file:
                json.dump(__process_status, process_file)

            with open("./test_process/account_stats.yml", "w") as account_stats_file:
                yaml.safe_dump(__account_stats, account_stats_file)

            __can_trade = False
