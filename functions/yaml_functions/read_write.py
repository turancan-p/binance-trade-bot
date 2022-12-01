import yaml

class ymlReadWrite():
    def __init__(self):
        self.symbols_file = "./settings/symbols.yml"
        self.client_file = "./settings/client.yml"
        self.status_settings_file = "./settings/status_settings.yml"
        self.process_status_file = "./data/process_data/process_status.yml"

    
    def read_file(self, target):
        with open(target, 'r') as file:
            loaded_file = yaml.load(file, Loader=yaml.FullLoader)
        return loaded_file
    
    def write_file(self, target, data):
        with open(target, 'w') as file:
            yaml.safe_dump(data, file)