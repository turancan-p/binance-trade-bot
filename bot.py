import timeit, time
from multiprocessing import Process

from settings.bot_settings import *
from collecting_functions.historical_data import HistoricalData
from collecting_functions.new_data import NewData
from test_process.test_trade_process import Trade


def collect_new_data():
    time.sleep(1)
    NewData().collect_new_data()

def trade_process():
    time.sleep(1)
    Trade().check_signals()


if __name__ == '__main__':
    program_start_time = timeit.default_timer()
    historical_collected = HistoricalData().collect_historical()
    program_process_finish_time = timeit.default_timer()
    
    print("")
    print("All Process Take:",program_process_finish_time - program_start_time, "Seconds")
    print("")
    print("Waiting for new datas..")
    
    if historical_collected == True:
        proces_1 = Process(target=collect_new_data)
        
        proces_2 = Process(target=trade_process)
        proces_1.start()
        proces_2.start()
