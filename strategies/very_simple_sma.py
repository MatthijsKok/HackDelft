import numpy as np
from simple_moving_average import simple_moving_average as sma
from check_with_previous import check_with_previous as cwp


class Strategy:

    def __init__(self, price_list, max_position=100):
        self.prices_list = price_list
        self.trades_list = np.zeros(len(price_list))
        self.max_pos = max_position
        self.min_pos = -max_position

        self.current_time = 0
        self.current_pos = 0

        # Execute strategy
        self.implement_strategy()

    def order(self, order_amount):
        # Calculate order amount
        actual_order_amount = np.clip(order_amount, self.min_pos - self.current_pos, self.max_pos - self.current_pos)

        # Execute the order
        self.trades_list[self.current_time] = actual_order_amount

    def order_until_at_position(self, position):
        self.order(position - self.current_pos)

    def update_position(self):
        self.current_pos = self.current_pos + self.trades_list[self.current_time]

    def implement_strategy(self):
        max_stock = 100
        min_stock = -100
        u = cwp(self.prices_list, 1000)
        v = cwp(self.prices_list, 100)
        w = cwp(self.prices_list, 10)
        z = cwp(self.prices_list, 1)
        last_second = len(self.prices_list) - 1
        for i, price in enumerate(self.prices_list):
            self.current_time = i
            # Reset your position at the end of the day
            if self.current_time == last_second:
                self.order_until_at_position(0)
            else:
                f = 0.4 * u[i] + 0.3 * v[i] + 0.2 * w[i] + 0.1 * z[i]
                current_stocks = self.current_pos
                if f > 0:
                    self.order((max_stock - current_stocks) * f * (price - self.prices_list[i - 1]))
                elif f < 0:
                    self.order((min_stock - current_stocks) * -f * (price - self.prices_list[i - 1]))

            self.update_position()
