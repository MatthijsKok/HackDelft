import numpy as np
import pandas


def simple_moving_average(price_list, window):
    """
    Takes a list of prices, and calculates the Simple Moving Average
    :param price_list: the list of prices
    :param window: the number of prices in the past you want to average
    :return: a list with SMA's at those indices
    """

    ret = np.cumsum(price_list)
    ret[window:] = ret[window:] - ret[:-window]

    #generate data for the first window - 1 data points
    head = np.zeros(window - 1)
    for i in range(window-1):
        head[i] = sum(price_list[0:i + 1]) / (i + 1)

    ret = ret[window - 1:] / window
    ret = [*head, *ret]
    return ret


print(simple_moving_average([1, 3, 5, 7, 9, 11], 3))

