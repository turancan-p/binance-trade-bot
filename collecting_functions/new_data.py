from datetime import datetime
from datetime import timedelta

from settings.bot_settings import *

import yaml
import timeit
import json
import websockets
import asyncio

class NewData():
    def __init__(self):
        self.symbol_list = SYMBOL_LIST
        self.exchange_pair = EXCHANGE_PAIR
        self.interval = INTERVAL
        self.new_dict = dict()
        self.response = asyncio.get_event_loop().run_until_complete(self.collect_new_data())

    async def collect_new_data(self):
        __stream_url = "wss://stream.binance.com:9443/ws/"
        __symbols = self.symbol_list
        __exchange_pair = self.exchange_pair
        __interval = self.interval
        __first_parameter = __symbols[0].lower()+__exchange_pair.lower() + "@kline_" + __interval
        __other_parameters = list()
        for symbol in __symbols[1:]:
            symbol = f'{symbol}{__exchange_pair}'
            __other_parameters.append(symbol.lower() + "@kline_" + __interval)
        __other_parameters = json.dumps(__other_parameters)
    
        async with websockets.connect(__stream_url + __first_parameter) as socket:
            __header = '{"method": "SUBSCRIBE", "params": ' + __other_parameters + ',  "id": 1}'

            await socket.send(__header)

            while True:
                self.response = await socket.recv()
                
                self.response = json.loads(self.response)
                __new_data = dict()
                
                if "e" in self.response:
                    __candle = self.response['k']
                    __date = datetime.fromtimestamp(int(str(__candle['T'])[:10]))
                    __date = __date.strftime('%d/%m/%Y %H:%M')
                    __symbol = __candle['s']
                    __open_price = float(__candle['o'])
                    __high_price = float(__candle['h'])
                    __low_price = float(__candle['l'])
                    __close_price = float(__candle['c'])
                    __is_candle_closed = float(__candle['x'])
                    if __is_candle_closed:
                        __new_data = [__date, __open_price, __high_price, __low_price, __close_price]
                        i = self.symbol_list.index(__symbol[:-(len(self.exchange_pair))])
                        self.new_dict[i] = __new_data
                        if len(self.new_dict)+1 == len(self.symbol_list):
                            start_time = timeit.default_timer()
                            with open("./data/all_data.json", 'r+') as file:
                                    loaded_file = json.load(file)
                            
                            for i in self.new_dict.keys():
                                print(self.symbol_list[i]+self.exchange_pair, self.new_dict[i])
                                loaded_file[self.symbol_list[i]+self.exchange_pair].append(self.new_dict[i])
                                
                            with open("./data/all_data.json", 'r+') as file:
                                file.seek(0)
                                json.dump(loaded_file, file)
                            self.new_dict.clear()
                            finish_time = timeit.default_timer()
                            print("")
                            print(f"New Data's collected and saved {finish_time - start_time} seconds")
                            print("")

                            with open("./settings/controller.yml", "r") as file:
                                controller = yaml.load(file, Loader=yaml.FullLoader)

                            controller["can_check_signals"] = True
                            
                            with open("./settings/controller.yml", "w") as file:
                                yaml.safe_dump(controller, file)