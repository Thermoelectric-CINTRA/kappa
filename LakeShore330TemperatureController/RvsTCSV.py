# from mpmath import *
# import numpy as np
# import pandas as pd
# import math
# # import csv
# import matplotlib.pyplot as plt
#
# #data
# filename = "D:\\Data Sorbonne University\\CINTRA 2018 -\\experimental plans\\Thermoelectrics\\setup\\RvsT measurement\\resistance_10K_to_475K.csv"
# df = pd.read_csv(filename)  #
#
# #plot
# plt.figure(1)
# ax1 = plt.gca()
# # ax2 = ax1.twiny()
# ax1.scatter(df['Temperature'], df['Resistances'], c='r', label='DC - 4 probes')
# # ax2.scatter(lock_in_temp, lock_in_mean, c='b', label='lock in')
# plt.xlabel('Temperature (K)')
# plt.ylabel('Mean resistance (Ohm)')
# plt.legend(loc='upper left')
#
#
# # #TCR
# # TCR_DC = (1/dc_mean[0])*(dc_mean[4]-dc_mean[0])/(dc_temp[4]-dc_temp[0])
# # TCR_AC = (1/lock_in_mean[0])*(lock_in_mean[4]-lock_in_mean[0])/(lock_in_temp[4]-lock_in_temp[0])
# # diff = 100*(TCR_DC - TCR_AC)/TCR_DC
# # print("TCR in DC heating:", TCR_DC, "\nTCR in AC heating:", TCR_AC)
# # print(diff)
#
# plt.show()

# fit a fifth degree polynomial to the economic data
from numpy import arange
from pandas import read_csv
from scipy.optimize import curve_fit
from matplotlib import pyplot
import pandas as pd

# # define the true objective function 5th polynomial
def objective(x, a, b, c, d, e, f):
    return (a * x) + (b * x ** 2) + (c * x ** 3) + (d * x ** 4) + (e * x ** 5) + f

# define the true objective function for linear regression fit
# def objective(x, a, b):
#     return a * x + b

# load the dataset
# url = 'https://raw.githubusercontent.com/jbrownlee/Datasets/master/longley.csv'
# filename = "D:\\Data Sorbonne University\\CINTRA 2018 -\\experimental plans\\Thermoelectrics\\setup\\RvsT measurement\\resistance_10K_to_475K.csv"
# data = pd.read_csv(filename)
fileName = "resistance_lockin.csv"
data = pd.read_csv('D:/CINTRA/kappa/LakeShore330TemperatureController/{}'.format(fileName))
# dataframe = read_csv(filename, header=None)
# data = dataframe.values
print(data)
# choose the input and output variables
# x, y = data[:, 4], data[:, -1]
x = data['Temperature']
y = data['X'] / data['Current']
# curve fit
popt, _ = curve_fit(objective, x, y)
# # summarize the parameter values 5th polynomial
a, b, c, d, e, f = popt
print('y = %.5f * x + %.5f * x^2 + %.5f * x^3 + %.5f * x^4+ %.5f * x^5 + %.5f' % (a, b, c, d, e, f))
# summarize the parameter values linear regression fit
# a, b = popt
# print('y = %.5f * x + %.5f' % (a, b))

# plot input vs output
pyplot.scatter(x, y)
# define a sequence of inputs between the smallest and largest known inputs
x_line = arange(min(x), max(x), 1)
# calculate the output for the range 5th order polynomial
y_line = objective(x_line, a, b, c, d, e, f)
# # calculate the output for the range linear regression
# y_line = objective(x_line, a, b)
# create a line plot for the mapping function
pyplot.plot(x_line, y_line, '--', color='red')
pyplot.show()