import matplotlib.pyplot as plt
from reader import read_all


prices = read_all()

prices_list = prices.price
print(prices_list)

# fig, ax = plt.subplots()
# plt.plot(ax=ax, title='Prices')
# plt.show()

plt.plot(prices_list)
plt.show()