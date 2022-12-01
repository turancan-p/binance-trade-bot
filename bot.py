from functions.collect_functions.collect_historical_functions import HistoricalData
from functions.collect_functions.collect_new_functions import NewData
from functions.yaml_functions.read_write import ymlReadWrite
from functions.indicator_functions.rsi import RsiCalculator
from functions.test_functions.test_trading_process import TestTrading

import timeit, time, os
import multiprocessing


def clear():
    os.system('cls')


def historical_data_process():
    start_time = timeit.default_timer()
    historical = HistoricalData()
    historical.collect_historical_data()
    finish_time = timeit.default_timer()
    print(f'Data collection process completed in  {finish_time - start_time} seconds')


def new_data_process():
    time.sleep(7)
    NewData().collect_new_data()


def strategy_process():
    rsi = RsiCalculator()
    yml = ymlReadWrite()
    strategy = TestTrading()
    symbols = yml.read_file(yml.symbols_file)['symbols']
    time.sleep(10)
    while True:
        yml = ymlReadWrite()
        can_search = yml.read_file(yml.status_settings_file)
        if can_search is not None:
            if can_search['can_search'] == True:
                start_time = timeit.default_timer()
                strategy.signal()
                finish_time = timeit.default_timer()
                can_search['can_search'] = False
                yml.write_file(yml.status_settings_file, can_search)
                print(f'Signal check process completed in  {finish_time - start_time} seconds')



if __name__ == '__main__':
    data = {"can_search": False, "number": 1}
    yml = ymlReadWrite()
    yml.write_file(yml.status_settings_file, data)
    process_1 = multiprocessing.Process(target=historical_data_process)
    process_2 = multiprocessing.Process(target=new_data_process)
    process_3 = multiprocessing.Process(target=strategy_process)

    process_1.start()
    process_2.start()
    process_3.start()

