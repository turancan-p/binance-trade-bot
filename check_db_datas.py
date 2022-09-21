from configs.config import SYMBOLS, TARGET_EXCHANCE, INTERVAL

from db.database import send_command_to_db
from db.commands import SELECT_COMMAND

for SYMBOL in SYMBOLS:
    datas = send_command_to_db(symbol=f'{SYMBOL}{TARGET_EXCHANCE}', interval=INTERVAL, command=SELECT_COMMAND)
    print(f'{SYMBOL}{TARGET_EXCHANCE}', INTERVAL)
    for data in datas:
        print(data)
        #return id, open, high, low, close