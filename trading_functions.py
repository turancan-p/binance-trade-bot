# buy coin function
# sell coin function


from functions.binance_functions.coin_details import CoinDetails
from functions.binance_functions.binance_client import BinanceClient
from functions.binance_functions.account_functions import AccountDetails

from binance.enums import *

class BinanceTrade:
    def __init__(self):
        self.current_client = BinanceClient()
        self.current_client = self.current_client.client()
        self.account_details = AccountDetails()
        self.buy_details = None
        self.sell_details = None

    def buy_coin_market_order(self, coin_symbol, exchange_pair):
        self.coin_details = CoinDetails(f'{coin_symbol}{exchange_pair}')
        __free_balance = self.account_details.get_free_balance(exchange_pair)
        print(type(__free_balance))
        print(__free_balance)
        __coin_amount = int(self.coin_details.amount_calculation(__free_balance)[0])
        print(__coin_amount)
        self.buy_details = self.current_client.order_market_buy(
            symbol = f'{coin_symbol}{exchange_pair}',
            quantity = __coin_amount
        )
        return self.buy_details

    def sell_coin_market_order(self, coin_symbol, exchange_pair):
        self.coin_details = CoinDetails(f'{coin_symbol}{exchange_pair}')
        __coin_amount = self.account_details.get_free_balance(coin_symbol)
        self.sell_details = self.current_client.order_market_sell(
            symbol = coin_symbol,
            quantity = __coin_amount
        )
        return self.sell_details

    def cancel_order(self, coin_symbol, exchange_pair, orderID):
        test = self.current_client.cancel_order(
            symbol = f'{coin_symbol}{exchange_pair}',
            orderId = orderID
        )
        return test

#print(BinanceTrade().buy_coin_market_order("TRX", "TRY"))