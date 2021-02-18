from mpmath import *
import numpy as np
import pandas as pd
import math
# import csv
import matplotlib.pyplot as plt


filename = "Data/resistance.csv"
# df = pd.read_excel('Sample3.xlsx')
df = pd.read_csv(filename)  # for 50 nm took data at 90 mA
# df = pd.read_excel('Sample3.xlsx', index_col ='Frequency')
# dc_mean = [16.466307000000004, 17.656899, 18.751384, 19.782772, 20.760893000000003, 21.639585999999998]
dc_mean = [17.656899, 18.751384, 19.782772, 20.760893000000003, 21.639585999999998]
# dc_temp = [301.1, 321, 340, 360, 379, 400]
dc_temp = [321, 340, 360, 379, 400]
# lock_in_mean = [, 16.52, 17.43, 18.24, 19.05, 19.7]
lock_in_mean = [16.52, 17.43, 18.24, 19.05, 19.7]
# lock_in_temp = [300, 320, 341, 360, 379.7, 380.2]
lock_in_temp = [320, 341, 360, 379.7, 400.1]

# create dataframe
# file = {
#     'Temperature': df['Temperature'],
#     'Mean Resistance DC': dc_mean,
#     'Mean Resistance Lock in': lock_in_mean,
# }
# data = pd.DataFrame(file)


# print(data)

#
# plt.figure(1)
# plt.subplot(1, 1, 1)
# fig = plt.figure()
ax1 = plt.gca()
ax2 = ax1.twiny()
ax1.scatter(dc_temp, dc_mean, c='r', label='DC')
ax2.scatter(lock_in_temp, lock_in_mean, c='b', label='lock in')
plt.xlabel('Temperature (K)')
plt.ylabel('Mean resistance (Ohm)')
# plt.xscale('log')
# plt.margins(x=0)
plt.legend(loc='upper left')

TCR_DC = (1/dc_mean[0])*(dc_mean[4]-dc_mean[0])/(dc_temp[4]-dc_temp[0])
TCR_AC = (1/lock_in_mean[0])*(lock_in_mean[4]-lock_in_mean[0])/(lock_in_temp[4]-lock_in_temp[0])

diff = 100*(TCR_DC - TCR_AC)/TCR_DC

print("TCR in DC:", TCR_DC, "\nTCR in AC:", TCR_AC)
print(diff)

plt.show()

