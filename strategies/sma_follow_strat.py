import numpy as np
import simple_moving_average as sma

def implement_strat(price_list):
    current_position = 0
    max_position = 100
    trade_list = np.zeros(len(price_list))
    sma10_list = sma.simple_moving_average(price_list, 10)
    sma200_list = sma.simple_moving_average(price_list, 200)
    for i, price in enumerate(price_list):
        # Go long
        if price < sma200_list[i]:
            # Buy
            if price > sma10_list[i]:
                trade_list[i] = max_position - current_position
                current_position = max_position
            # Stoploss
            else:
                trade_list[i] = -current_position
                current_position = 0
        # Go short
        else:
            # Sell
            if price < sma10_list[i]:
                trade_list[i] = -max_position - current_position
                current_position = -max_position
            # Stoploss
            else:
                trade_list[i] = -current_position
                current_position = 0
    return trade_list