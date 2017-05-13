import matplotlib.pyplot as plt
from reader import *
import numpy as np

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

# Trend lines for different averages
trends = [1, 10, 300]

# Calculate trend lines
for trend in trends:
    trend_line = np.convolve(prices_list, np.ones(trend) / trend, mode='full')
    trend_line = trend_line[max(trends): len(trend_line) - max(trends)]
    plt.plot(trend_line)

# Show plot
plt.legend(trends, loc='lower center')
plt.title("Price with trend lines")
plt.show()

