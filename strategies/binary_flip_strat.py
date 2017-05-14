import numpy as np
from simple_moving_average import simple_moving_average as sma


class Strategy:

    def __init__(self, price_list, max_position=100):
        self.prices_list = price_list
        self.trades_list = np.zeros(len(price_list))
        self.position_list = np.zeros(len(price_list))
        self.max_position = max_position
        self.min_position = -max_position

        # Execute strategy
        self.implement_strategy()

    def order(self, time, order_amount):
        current_position = self.position_list[time]
        desired_position = current_position + order_amount
        if desired_position < -100:
            actual_order_amount = self.min_position - current_position
        elif desired_position > 100:
            actual_order_amount = self.max_position - current_position
        else:
            actual_order_amount = order_amount
        self.trades_list[time] = actual_order_amount

    def order_until_at_position(self, time, position):
        current_position = self.position_list[time]
        self.order(time, (position - current_position))

    def update_position(self, time):
        self.position_list[time] = self.position_list[time-1] + self.trades_list[time-1]

    def implement_strategy(self):
        for i, price in enumerate(self.prices_list):
            self.update_position(i)

            previous_price = self.prices_list[i-1]

            if previous_price > price:
                self.order_until_at_position(i, 100)
            elif previous_price == price:
                self.order_until_at_position(i, 0)
            else:
                self.order_until_at_position(i, -100)

            # Reset your position at the end of the day
            if i == len(self.prices_list)-1:
                self.order_until_at_position(len(self.prices_list)-1, 0)
