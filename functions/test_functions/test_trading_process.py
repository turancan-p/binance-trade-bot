from functions.json_functions.read_write import jsonReadWrite
from functions.yaml_functions.read_write import ymlReadWrite
from functions.test_functions.test_strategy import TestStrategy
from functions.test_functions.test_buy_sell import TestBuySell


class TestTrading():
    def __init__(self):
        self.json_functions = jsonReadWrite()
        self.yml_functions = ymlReadWrite()
        self.strategy = TestStrategy()
        self.buy_sell_functions = TestBuySell()
        __account_stats = self.json_functions.read_file(self.json_functions.account_data_file)
        self.start_budget = __account_stats['budget']        
        

    def signal(self):
        __signal, __symbol = self.strategy.strategy()
        self.status = self.yml_functions.read_file(self.yml_functions.process_status_file)
   
        if __signal == "BUY" and __symbol is not None and self.status['in_position'] == False:
            self.buy_sell_functions.buy(__symbol)
        elif self.status['in_position'] == True:
             self.buy_sell_functions.sell()
             
        self.buy_sell_functions.write_console()