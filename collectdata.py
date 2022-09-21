import data.historical_data as historical
from configs.config import TARGET_EXCHANCE, INTERVAL, HIST_MAX_NEED, SYMBOLS

for symbol in SYMBOLS:
    historical.save_historical_to_db(symbol, TARGET_EXCHANCE, INTERVAL, HIST_MAX_NEED)