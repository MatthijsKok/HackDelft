#!/home/balint/virtualenvs/py34/bin/python
import numpy as np
import os
import pandas as pd
from tqdm import tqdm


def trade_generator(max_lots=100, close_by=30601):

    # The number of stocks you would like to trade
    trade = 0
    # Number of trades in possession
    pos = 0
    # Number of the trade (the second of the day)
    nr = 0

    while True:
        nr += 1
        next_price = yield trade

        # If it is the last second of the day, sell everything you have, so you end the day with 0 stocks
        if nr == close_by:
            trade = -pos
        # Else, generate a random number from a normal distribution to to trade of sell
        else:
            desired_trade = np.round(np.random.normal(loc=0, scale=5))
            # If the trade generated would cause the number of stocks in possession to be bigger or smaller than the
            # maximum number you can own (100), adjust for it
            if pos + desired_trade > max_lots:
                trade = max_lots - pos
            elif pos + desired_trade < -1 * max_lots:
                trade = -1 * pos - max_lots
            # Else, trade the specified amount
            else:
                trade = desired_trade

        # Add the number traded to the stocks in possession
        pos += trade


# Create a list with all file names in the directory
day_prices = [f for f in os.listdir('./prices/') if '_prices.csv' in f]


# Sort the list so the dates are sorted
day_prices.sort()

# For each data file..
for price_filename in tqdm(day_prices):
    # Read in the file, indexed on time
    dataframe = pd.read_csv("./prices/" + price_filename, index_col='times', parse_dates=True)

    # Get the list of prices
    c = dataframe['price'].values

    # Get the length of the list of prices
    l = len(c)

    # Generate trades for the day
    g = trade_generator(max_lots=100, close_by=l)
    g.send(None)

    # Generate an array containing only zeros, with same length as the number of trades (30601)
    pos = np.zeros(l)

    # Fill in the array with the trades
    for i in range(l):
        pos[i] = g.send(c[i])

    # Write trades to file
    trade_filename = os.path.join('./trades/', price_filename.replace('prices', 'trades'))
    pd.DataFrame(index=dataframe.index, columns=['trades'], data=pos).to_csv(trade_filename)
