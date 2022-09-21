import uuid

from helpers.binance_client import get_historical_klines as history
from db.database import send_command_to_db, create_db
from db.commands import INSERT_COMMAND


def save_historical_to_db(symbol, target_exchance, interval, max_need):
    create_db(f'{symbol}{target_exchance}', interval)
    datas = history(symbol, target_exchance, interval, max_need)
    datas.pop()
    for data in datas:
        # 0=open time, 1=open price, 2= High price, 3=Low price, 4= close price, 5= volume
        id = str(uuid.uuid4().hex)
        open = data[1]
        high = data[2]
        low = data[3]
        close = data[4]
        new_Data = [id, open, high, low, close]
        send_command_to_db(f'{symbol}{target_exchance}', interval, INSERT_COMMAND, new_Data)
    print("All Data Saved To DB")
