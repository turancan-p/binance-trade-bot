import sqlite3
from settings.configs import TARGET_EXCHANCE

CREATE_COMMAND = '''CREATE TABLE IF NOT EXISTS Data (Open real, High real, Low real, Close real)'''

INSERT_COMMAND = "INSERT INTO Data (Open, High, Low, Close) values (?, ?, ?, ?)"

SELECT_COMMAND = "SELECT * FROM Data"

DELETE_COMMAND = "DELETE FROM Data"


def create_db(symbol, interval):
    connection = sqlite3.connect(f'{symbol.lower()+TARGET_EXCHANCE.lower()}@kline_{interval}.db')
    connection_cursor = connection.cursor()

    connection_cursor.execute(CREATE_COMMAND)
    connection_cursor.execute(DELETE_COMMAND)

    connection_cursor.fetchall()

    connection.commit()
    connection_cursor.close()
    connection.close()
    print("SqLite3 db created for: ", symbol, interval)


def insert_new_data(symbol, interval, data):
    connection = sqlite3.connect(f'{symbol.lower()}@kline_{interval}.db')
    connection_cursor = connection.cursor()

    response = connection_cursor.execute(INSERT_COMMAND, data)
    response.fetchone()

    connection.commit()
    connection_cursor.close()
    connection.close()


def select_all_data(symbol, interval):
    connection = sqlite3.connect(f'{symbol.lower()+TARGET_EXCHANCE.lower()}@kline_{interval}.db')
    connection_cursor = connection.cursor()
    connection_cursor.execute(SELECT_COMMAND)
    response = connection_cursor.fetchall()[-1]

    connection.commit()
    connection_cursor.close()
    connection.close()

    return response
