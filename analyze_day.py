#!/home/balint/virtualenvs/py34/bin/python
import argparse
import numpy as np
import matplotlib.pyplot as plt
from reader import *

"""
Reads all prices, assumed to be named like 2017-01-03_prices.csv
Reads all trades, assumed to be named like 2017-01-03_trades.csv

Prices should be formatted like:
times,price
2017-01-04 09:00:00,3052.03
2017-01-04 09:00:01,3051.94
2017-01-04 09:00:02,3052.12

Trades should be formatted like:
times,trades
2017-01-04 09:00:00,-2.0
2017-01-04 09:00:01,-2.0
2017-01-04 09:00:02,-1.0

Every second is assumed to have a trade, even if it's zero

"""

# day to analyze
day = 3


def analyze_day(day=1):
    parser = argparse.ArgumentParser(description='Evaluate trades')
    parser.add_argument(
        "-t", "--teamname", help="Name of the team for outputting results", metavar="TEAMNAME", default='Test Team')
    parser.add_argument(
        "-p", "--plot", help="Show the profit plot after evaluating", action='store_true'
    )

    transaction_cost = 0.0
    prices = read_day(day)
    print('All prices read')
    trades = read_day(day, '_trades.csv', 'trades')
    print('All trades read')

    prices['trades'] = trades
    prices['position'] = prices.trades.cumsum()
    prices['invested'] = prices.position * prices.price
    prices['trade_cost'] = prices.trades * prices.price
    prices['transaction_cost'] = np.abs(prices.trades) * transaction_cost
    prices['cum_transaction_cost'] = prices.transaction_cost.cumsum()
    prices['PnL'] = (prices.trade_cost - prices.transaction_cost)
    prices['cum_pnl'] = prices.PnL.cumsum() - (prices.price * prices.position)

    positive_pos = (prices.position >= 0) * prices.price
    negative_pos = (prices.position <= 0) * prices.price
    neutral_pos = (prices.position == 0) * prices.price

    # Connect line segments
    for i in range(len(positive_pos)):
        value_diff = positive_pos[i - 1] - positive_pos[i]
        if positive_pos[i] == 0 and value_diff > 0:
            positive_pos[i] = negative_pos[i]

    positive_pos[:] = [x if x != 0 else np.nan for x in positive_pos]
    negative_pos[:] = [x if x != 0 else np.nan for x in negative_pos]
    neutral_pos[:] = [x if x != 0 else np.nan for x in neutral_pos]

    # print((prices.position >= 0) * prices.price)

    # positive_pos[prices.position >= 0] = np.nan
    # negative_pos[prices.position < 0] = np.nan

    print(positive_pos)
    print(negative_pos)

    ax = plt.subplot(211)
    ax.set_title("Prices")
    plt.plot(positive_pos, 'g')
    plt.plot(negative_pos, 'r')
    plt.plot(neutral_pos, 'b')
    ax = plt.subplot(212)
    ax.set_title("Profit/Loss")
    plt.plot(prices.cum_pnl)
    plt.show()


analyze_day(day)
