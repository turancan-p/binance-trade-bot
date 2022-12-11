#get account balance details
#get account free balance
#get account coin balance

from functions.binance_functions.binance_client import BinanceClient


class AccountDetails:
    def __init__(self):
        self.current_client = BinanceClient()
        self.current_client = self.current_client.client()

    def get_free_balance(self, symbol):
        __balance = self.current_client.get_asset_balance(symbol)
        float(__balance['free'])
        return float(__balance['free'])