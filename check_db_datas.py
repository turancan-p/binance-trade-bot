from configs.config import SYMBOL, TARGET_EXCHANCE, INTERVAL

from db.database import send_command_to_db
from db.commands import SELECT_COMMAND

datas = send_command_to_db(SYMBOL + TARGET_EXCHANCE, INTERVAL, SELECT_COMMAND)

for data in datas:
    print(data)
    #return id, open, high, low, close