import json
import asyncio
import websockets

from settings.configs import TARGET_EXCHANCE, INTERVAL, SYMBOLS
from sqlite3_db.database import insert_new_data
from collect_data.collect_historical import collect as historical_data_collect
from sqlite3_db.get_data_from_db import write_console

stream_url = "wss://stream.binance.com:9443/ws/"


async def test():
    new_list = []
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
                    #TODO call signal function and do buy or sell

asyncio.get_event_loop().run_until_complete(test())
