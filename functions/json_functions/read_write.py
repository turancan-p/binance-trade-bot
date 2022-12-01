import json

class jsonReadWrite():
    def __init__(self):
        self.all_coins_data_file = "./data/coin_data/all_data.json"
        self.account_data_file = "./data/account_data/account_stats.json"

    def read_file(self,target_file):
        with open(target_file, 'r') as file:
            __data_file = json.load(file)
        return __data_file
    
    def write_file(self, target_file, data):
        with open(target_file, 'w') as file:
            json.dump(data, file)

    def update_file(self, target_file, data, key):
        with open(target_file, 'r+') as file:
            loaded_file = json.load(file)
            loaded_file[key].append(data)
            file.seek(0)
            json.dump(loaded_file, file)
