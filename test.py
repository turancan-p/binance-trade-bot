from binance_functions.functions import get_price, amount_calc


symbol = "trxusdt"

budget = 1000

quantity, budget = amount_calc(symbol, budget, get_price(symbol))

print(quantity, budget)

