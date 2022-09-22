import numpy

from configs.config import SYMBOLS, TARGET_EXCHANCE, INTERVAL

from db.database import send_command_to_db
from db.commands import SELECT_COMMAND
import indicators.talib_indicators as indicator

def get_datas(symbol):
    newlist = []
    datas_ = send_command_to_db(symbol=f'{symbol}{TARGET_EXCHANCE}', interval=INTERVAL, command=SELECT_COMMAND)
    # return id, open, high, low, close
    for data_ in datas_:
        newlist.append(data_)
    return newlist