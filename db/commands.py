# 0=open time, 1=open price, 2= High price, 3=Low price, 4= close price, 5= volume
CREATE_COMMAND = '''CREATE TABLE IF NOT EXISTS Data (id text, Open real, High real, Low real, Close real)'''

INSERT_COMMAND = "INSERT INTO Data (id, Open, High, Low, Close) values (?, ?, ?, ?, ?)"

SELECT_COMMAND = "SELECT * FROM Data"

DELETE_COMMAND = "DELETE FROM Data"