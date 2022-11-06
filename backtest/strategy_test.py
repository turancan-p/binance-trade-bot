import talib, numpy
import pandas as pd
import os

csv_files = ['BTC@kline_1m', 'ETH@kline_1m', 'BNB@kline_1m']

dataframe = pd.read_csv(f'{csv_files[0]}.csv')

close_values = []
index = 0

budget = 100
last_budget = budget
starting_budget = budget

win = 0
win_rate = None

coin_amount = 0

process_count = 0
in_position = False


def clear_console():
    os.system('cls')


def buy(budget, closeVal):
    coin_amount = budget / closeVal
    return coin_amount


def sell(coin_amount, closeVal):
    global process_count
    budget = coin_amount * closeVal
    process_count += 1
    return budget


def percentage(part, whole):
    perc = 100 * (int(part) / int(whole))
    return int(perc)


for x in range(1, len(dataframe), 1):
    index = index + 1
    csv_index = dataframe[x:x + 1]
    close_value = float(csv_index['Close'])

    close_values.append(close_value)
    numpy_closes = numpy.array(close_values)

    if index > 20:
        rsi_20 = talib.RSI(numpy_closes, 20)
        last_rsi_20 = rsi_20[-1]

    if index > 100:
        ema_50 = talib.EMA(numpy_closes, 20)
        ema_200 = talib.EMA(numpy_closes, 100)
        last_ema_50 = ema_50[-1]
        last_ema_200 = ema_200[-1]

        if last_rsi_20 < 30:
            if not in_position:
                if last_ema_50 < last_ema_200:
                    print("Oversold! Buying BTC this price: ", close_value)

                    coin_amount = buy(budget, close_value)

                    budget = 0
                    in_position = True

        if last_rsi_20 > 70:
            if in_position:
                if last_ema_50 > last_ema_200:
                    clear_console()
                    print("Overbought! Selling BTC this price: ", close_value)

                    if last_budget < (coin_amount * close_value):
                        win += 1

                    budget = sell(coin_amount, close_value)
                    last_budget = budget

                    win_rate = percentage(win, process_count)

                    coin_amount = 0
                    print("Budget: ", budget)
                    print("---------------------------------------------------")
                    print('Total process: ', process_count, 'PNL: ', budget - starting_budget, 'Win rate: %', win_rate)
                    print("---------------------------------------------------")
                    in_position = False
