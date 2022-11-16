import json
import asyncio
import websockets

from binance_functions.functions import test_buy, test_sell, win_rate_calc
from settings.configs import TARGET_EXCHANCE, INTERVAL, SYMBOLS
from settings import configs
from sqlite3_db.database import insert_new_data
from collect_data.collect_historical import collect as historical_data_collect
from sqlite3_db.get_data_from_db import write_console, write_details
from strategy import test_strategy
from discord.discord_functions import send_message

stream_url = "wss://stream.binance.com:9443/ws/"


async def collect_data():
    new_list = []
    message = ""
    for symbol in SYMBOLS:
        new_list.append(f'{symbol.lower()}{TARGET_EXCHANCE.lower()}@kline_{INTERVAL}')

    historical_data_collect()

    first_pair = new_list[0]
    new_list.pop(0)

    new_list = json.dumps(new_list)

    async with websockets.connect(stream_url + first_pair) as sock:
        pairs = '{"method": "SUBSCRIBE", "params": ' + new_list + ',  "id": 1}'  # other pairs

        await sock.send(pairs)

        while True:
            response = await sock.recv()

            response = json.loads(response)

            if "e" in response:
                candle = response['k']
                symbol = candle['s']
                open = candle['o']
                high = candle['h']
                low = candle['l']
                close = candle['c']
                is_candle_closed = candle['x']
                if is_candle_closed:
                    new_data = (open, high, low, close)
                    insert_new_data(symbol, INTERVAL, new_data)
                    write_console()
                    signals = test_strategy.run_strategy()

                    for symb in SYMBOLS:
                        if configs.IN_POSITION is False and signals[symb + TARGET_EXCHANCE] == "WAIT":
                            print("Looking position for:", symb)

                        elif configs.IN_POSITION is True and signals[configs.CURRENT_COIN] == "WAIT":
                            print("Looking sell position for:", configs.CURRENT_COIN)

                        elif configs.IN_POSITION is True and signals[configs.CURRENT_COIN] == "BUY":
                            print("HOLD:", configs.CURRENT_COIN)

                        elif configs.IN_POSITION is False and signals[symb + TARGET_EXCHANCE] == "BUY":
                            print("BUY:", symb)
                            configs.COIN_AMOUNT, configs.BUDGET = test_buy(configs.BUDGET, close), 0
                            configs.CURRENT_COIN = symb + TARGET_EXCHANCE

                            message = send_message(configs.CURRENT_COIN, "BUY", configs.BUDGET, configs.COIN_AMOUNT, close, configs.PROCESS_COUNT, configs.PNL, configs.WIN_RATE)
                            print("buy:", message)
                            configs.IN_POSITION = True

                        elif configs.IN_POSITION is True and signals[configs.CURRENT_COIN] == "SELL":
                            print("SELL:", symb)
                            (configs.BUDGET, configs.PROCESS_COUNT), configs.COIN_AMOUNT = test_sell(configs.COIN_AMOUNT, close, configs.PROCESS_COUNT), 0
                            if configs.LAST_BUDGET < configs.BUDGET:
                                configs.WIN_COUNT += 1
                            configs.WIN_RATE = win_rate_calc(configs.WIN_COUNT, configs.PROCESS_COUNT)
                            configs.PNL = configs.BUDGET - configs.START_BUDGET

                            message = send_message(configs.CURRENT_COIN, "SELL", configs.BUDGET, configs.COIN_AMOUNT, close, configs.PROCESS_COUNT, configs.PNL, configs.WIN_RATE)
                            print("sell:", message)
                            configs.IN_POSITION = False

                    print(message)
                    print("")
                    if configs.COIN_AMOUNT == 0:
                        configs.CURRENT_COIN = "None"
                    write_details(configs.BUDGET, configs.CURRENT_COIN, configs.COIN_AMOUNT, configs.PNL, configs.PROCESS_COUNT, configs.WIN_RATE)


asyncio.get_event_loop().run_until_complete(collect_data())
