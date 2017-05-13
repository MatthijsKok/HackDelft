import matplotlib.pyplot as plt
from reader import read_all
import numpy as np

# Read in prices files
prices = read_all()

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

