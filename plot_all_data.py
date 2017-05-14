import matplotlib.pyplot as plt
from reader import *
import numpy as np
from simple_moving_average import simple_moving_average as sma
import pandas

# True if you want to plot al 50 days, false if you want to plot a single day
plot_all = False

# The day (1 to 50) you want to plot
day = 1

# Read in prices files
if plot_all:
    prices = read_all()
else:
    prices = read_day(day)

# Get the prices from the file
prices_list = prices.price
prices_list = pandas.Series.tolist(prices_list)

# Trend lines for different averages
trend_windows = [1, 10, 100]

# Calculate trend lines
for window in trend_windows:
    trend_line = np.convolve(prices_list, np.ones(window) / window, mode='full')
    sma_line = sma(prices_list, window)
    plt.plot(sma_line)

# Show plot
plt.legend(trend_windows, loc='lower center')
plt.title("Price with trend lines")
plt.show()

