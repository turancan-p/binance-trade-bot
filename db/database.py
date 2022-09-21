import sqlite3
from db.commands import *


def send_command_to_db(symbol, interval, command, data=None):
    connection = sqlite3.connect(f'{symbol}{interval}.db')
    connection_cursor = connection.cursor()

    if data is None:
        connection_cursor.execute(command)
        response = connection_cursor.fetchall()
    else:
        response = connection_cursor.execute(command, data)
        response.fetchone()

    connection.commit()
    connection.close()

    return response if response else None


def create_db(symbol, interval):
    connection = sqlite3.connect(f'{symbol}{interval}.db')
    connection_cursor = connection.cursor()

    connection_cursor.execute(CREATE_COMMAND)
    connection_cursor.fetchone()

    connection_cursor.execute(DELETE_COMMAND)
    connection_cursor.fetchone()

    connection.commit()
    connection.close()
    print("Database Created For: ", symbol, interval)
