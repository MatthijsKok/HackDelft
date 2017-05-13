import numpy as np


def simple_moving_average(price_list, window):
    """
    Takes a list of prices, and calculates the Simple Moving Average
    :param price_list: the list of prices
    :param window: the number of prices in the past you want to average
    :return: a list with SMA's at those indices
    """
    averages_list = np.zeros(len(price_list))
    for i, price in enumerate(price_list):
        averages_list[i] = np.mean(price_list[max(0, i - window):i])
    return averages_list
