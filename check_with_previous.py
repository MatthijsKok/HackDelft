import numpy as np
import logging


def check_with_previous(the_list, window):
    amount = 0
    checked = 0
    compare_list = np.zeros(len(the_list))
    for i in range(0, len(the_list)):
        for j in range(1, window):
            if the_list[i - j] < the_list[i]:
                amount = amount - 1
            elif the_list[i - j] > the_list[i]:
                amount = amount + 1
            checked = checked + 1
        compare_list[i] = amount / checked
    return compare_list

some_list = [4, 10, 2, 20, 15, 3, 3]
logging.debug(check_with_previous(some_list, 1))