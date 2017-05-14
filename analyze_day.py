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
day = 10

def analyze_day(day=1):
    parser = argparse.ArgumentParser(description='Evaluate trades')
    parser.add_argument(
        "-t", "--teamname", help="Name of the team for outputting results", metavar="TEAMNAME", default='Test Team')
    parser.add_argument(
        "-p", "--plot", help="Show the profit plot after evaluating", action='store_true'
    )
    args = parser.parse_args()

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

    # daily_sums = prices.groupby(pd.TimeGrouper('1D')).agg({'cum_pnl': 'last', 'position': 'last', 'PnL': 'sum', 'transaction_cost':'sum'}).dropna()
    #
    # mean_daily_pnl = daily_sums.PnL.mean()
    # std_daily_pnl = daily_sums.PnL.std()
    # min_daily_pnl = daily_sums.PnL.min()
    # max_daily_pnl = daily_sums.PnL.max()
    # min_position = prices.position.min()
    # max_position = prices.position.max()
    # positions_not_closed = (daily_sums.position != 0).sum()
    # print('Mean daily pnl: ', mean_daily_pnl, 'std of daily pnl', std_daily_pnl, ' min daily pnl: ', min_daily_pnl, 'max daily pnl: ', max_daily_pnl)
    # print('Positions not closed ', positions_not_closed, ' times. ')
    # print('Min position: ', min_position, ' max position: ', max_position)

    # daily_sums.to_csv('Results_' + str(args.teamname) + '.csv')

    ax = plt.subplot(211)
    ax.set_title("Prices")
    plt.plot(prices.price)
    ax = plt.subplot(212)
    ax.set_title("Profit/Loss")
    plt.plot(prices.cum_pnl)
    plt.show()


analyze_day(day)
