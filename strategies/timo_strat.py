import numpy as np
import simple_moving_average as sma


class Strategy:

    def __init__(self, price_list, max_position=100):
        self.prices_list = price_list
        self.trades_list = np.zeros(len(price_list))
        self.position_list = np.zeros(len(price_list))
        self.max_position = max_position
        self.min_position = -max_position

        # Execute strategy
        self.implement_strategy()

        # print(self.prices_list)
        # print(self.trades_list)
        # print(self.position_list)

    def order(self, time, order_amount):
        # print()
        # print('ORDERING...')
        # print('at time: {} wanted order of {}: '.format(time, order_amount))
        current_position = self.position_list[time-1]
        # print('current position: {}'.format(current_position))
        desired_position = current_position + order_amount
        # print('desired position: {}'.format(desired_position))
        if desired_position < -100:
            actual_order_amount = self.min_position - current_position
        elif desired_position > 100:
            actual_order_amount = self.max_position - current_position
        else:
            actual_order_amount = order_amount
        # print('actual order amount: {}'.format(actual_order_amount))
        self.trades_list[time] = actual_order_amount
        self.position_list[time] = current_position + actual_order_amount

        # print('FINISHED ORDER!!!')
        # print()

    def order_until_at_position(self, time, position):
        # print('ordering until at position: {}'.format(position))
        # print('current position: {}'.format(self.position_list[time]))

        current_position = self.position_list[time]
        self.order(time, (position - current_position))

        # print('new position: {}'.format(self.position_list[time]))
        # print()

    def implement_strategy(self):
        sma10_list = sma.simple_moving_average(self.prices_list, 10)
        sma200_list = sma.simple_moving_average(self.prices_list, 200)
        for i, price in enumerate(self.prices_list):
            if price > sma200_list[i]:
                if price > sma10_list[i]:
                    self.order_until_at_position(i, 0)
                else:
                    self.order_until_at_position(i, 100)
            else:
                if price > sma10_list[i]:
                    self.order_until_at_position(i, -100)
                else:
                    self.order_until_at_position(i, 0)
