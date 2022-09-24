import asyncio
import json
import uuid
import websockets

from configs.config import TARGET_EXCHANCE, INTERVAL, HIST_MAX_NEED, SYMBOLS
from data.historical_data import save_historical_to_db
from db.commands import INSERT_COMMAND
from db.database import send_command_to_db
from talib_signals import signals

for symbol_ in SYMBOLS:
    save_historical_to_db(symbol=symbol_, target_exchance=TARGET_EXCHANCE, interval=INTERVAL, max_need=HIST_MAX_NEED)


async def save_new_data_to_db():
    list = []
    for symbol_ in SYMBOLS:
        list.append(f'{symbol_.lower()}{TARGET_EXCHANCE.lower()}@kline_{INTERVAL}')

    first_pair = list[0]
    list.pop(0)

    newlist = json.dumps(list)

    stream_url = "wss://stream.binance.com:9443/ws/"  # steam address

    async with websockets.connect(stream_url + first_pair) as sock:
        pairs = '{"method": "SUBSCRIBE", "params": ' + newlist + ',  "id": 1}'  # other pairs

        await sock.send(pairs)

        while True:
            response = await sock.recv()

            response_json = json.loads(response)
            if 'k' in response_json:
                id = str(uuid.uuid4().hex)
                candle = response_json['k']
                symbol = candle['s']
                open = candle['o']
                high = candle['h']
                low = candle['l']
                close = candle['c']
                is_candle_closed_ = candle['x']

                if is_candle_closed_:
                    new_data = [id, open, high, low, close]
                    send_command_to_db(symbol, INTERVAL, INSERT_COMMAND, new_data)
                    print("New Data Saved To DB For: ", symbol, INTERVAL)
                    signals()
                else:
                    print("Data Received!")


asyncio.get_event_loop().run_until_complete(save_new_data_to_db())
