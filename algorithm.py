#!/home/balint/virtualenvs/py34/bin/python
import os
import pandas as pd
from tqdm import tqdm

# Define the strat you want to use here.
# all strat files must have implement_strat(price_list) -> trades_list
from strategies import average_trading as strategy


def calculate_trades(price_list):
    s = strategy.Strategy(price_list)
    return s.trades_list

for f in os.listdir('./trades/'):
    file_path = os.path.join('./trades/', f)
    try:
        if os.path.isfile(file_path):
            os.unlink(file_path)
    except Exception as e:
        print(e)

# Create a list with all file names in the directory
day_prices = [f for f in os.listdir('./prices/') if '_prices.csv' in f]
# Sort the list so the dates are sorted
day_prices.sort()
# day_prices = day_prices[0:10]
# For each data file..h
for price_filename in tqdm(day_prices):
    # Read in the file, indexed on time
    dataframe = pd.read_csv("./prices/" + price_filename, index_col='times', parse_dates=True)
    # Get the list of prices
    c = dataframe['price'].values
    # Calculate trades
    pos = calculate_trades(c)
    # Write trades to file
    trade_filename = os.path.join('./trades/', price_filename.replace('prices', 'trades'))
    pd.DataFrame(index=dataframe.index, columns=['trades'], data=pos).to_csv(trade_filename)
