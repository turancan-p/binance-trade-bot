from binance.client import Client

class CreateClient():
    def __init__(self, api_key = "", secret_key = ""):
        self.api_key = api_key
        self.secret_key = secret_key

    def client(self):
        __client = Client(self.api_key, self.secret_key)
        return __client