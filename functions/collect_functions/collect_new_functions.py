from functions.yaml_functions.read_write import ymlReadWrite
from functions.json_functions.read_write import jsonReadWrite
from functions.collect_functions import new_data_helper as sthelper

from datetime import datetime

import json
import websockets
import asyncio


class NewData():
    def __init__(self):
        self.yml_functions = ymlReadWrite()
        self.json_functions = jsonReadWrite()
        self.response = asyncio.get_event_loop().run_until_complete(self.collect_new_data())
        
    async def collect_new_data(self):
        __stream_url = "wss://stream.binance.com:9443/ws/"
        __symbols = self.yml_functions.read_file(self.yml_functions.symbols_file)['symbols']
        __interval = self.yml_functions.read_file(self.yml_functions.symbols_file)['interval']
        __first_parameter = __symbols[0].lower() + "@kline_" + __interval
        __other_parameters = list()
        for symbol in __symbols[1:]:
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
                    __date = datetime.fromtimestamp(int(str(__candle['T'])[:10])).strftime('%d/%m/%Y %H:%M')
                    __symbol = __candle['s']
                    __open_price = float(__candle['o'])
                    __high_price = float(__candle['h'])
                    __low_price = float(__candle['l'])
                    __close_price = float(__candle['c'])
                    __is_candle_closed = float(__candle['x'])

                    if __is_candle_closed:
                        __yml = ymlReadWrite()
                        __yml_data = __yml.read_file(__yml.status_settings_file)
                        __yml_data['can_search'] = False
                        __yml.write_file(__yml.status_settings_file, __yml_data)
                        __new_data = [__date, __open_price, __high_price, __low_price, __close_price]
                        print(__symbol)
                        print(__new_data)
                        self.json_functions.update_file(self.json_functions.all_coins_data_file,__new_data, __symbol)  
                        
                        if sthelper.collected_number != len(__symbols):
                            sthelper.collected_number += 1
                            print(sthelper.collected_number)
                            if sthelper.collected_number == (len(__symbols)):
                                sthelper.collected_number = 0
                                print(sthelper.collected_number)
                                __yml_data['can_search'] = True
                                __yml.write_file(__yml.status_settings_file, __yml_data)
