import talib
import numpy
from numpy import genfromtxt

my_data = genfromtxt('5minutes.csv', delimiter=',')
price = my_data[:, 4]

exponential_moving_average = talib.EMA(price, timeperiod=8)

print(exponential_moving_average)

rsi = talib.RSI(price, timeperiod=7)
print(rsi)