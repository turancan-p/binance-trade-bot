from binance.client import Client
from functions.yaml_functions.read_write import ymlReadWrite


class BinanceClient:
    def __init__(self):
        self.yml = ymlReadWrite()

    def client(self):
        __client_data = self.yml.read_file(self.yml.client_file)
        __client = Client(__client_data['api_key'], __client_data['api_secret'])
        return __client
        