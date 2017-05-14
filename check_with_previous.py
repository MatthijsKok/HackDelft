import numpy as np


def check_with_previous(the_list, window):
    compare_list = np.zeros(len(the_list))
    for i in range(window, len(the_list)):
        amount = 0
        checked = 0
        for j in range(1, window + 1):
            if the_list[i - j] < the_list[i]:
                amount = amount - 1
            elif the_list[i - j] > the_list[i]:
                amount = amount + 1
            checked = checked + 1
        compare_list[i] = amount / checked
    return compare_list
