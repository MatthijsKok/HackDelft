import simple_moving_average as sma
import logging

list1 = [0, 1, 2, 3, 4, 5, 6]
sma_list1 = sma.simple_moving_average(list1, 3)
print(sma_list1)

if sma_list1[3] != 2:
    logging.error("Wrong!")
