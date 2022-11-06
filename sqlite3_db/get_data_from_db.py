from sqlite3_db.database import select_all_data
from settings.configs import SYMBOLS, INTERVAL, TARGET_EXCHANCE
import os
from prettytable import PrettyTable


def clear_console():
    os.system('cls')


def write_console():
    clear_console()
    for symbol in SYMBOLS:
        my_table = PrettyTable()
        my_table.field_names = ["Symbol", "Open Price", "High Price", "Low Price", "Close Price"]
        data = select_all_data(symbol, INTERVAL)
        my_table.add_row([symbol+TARGET_EXCHANCE, str(data[0]), str(data[1]), str(data[2]), str(data[3])])
        print(my_table)
