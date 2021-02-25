import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import datetime

# fileName1 = "resistance_front.csv"
# fileName2 = "resistance_rear.csv"
# data1 = pd.read_csv('D:/CINTRA/kappa/LakeShore330TemperatureController/Data/{}'.format(fileName1))
# data2 = pd.read_csv('D:/CINTRA/kappa/LakeShore330TemperatureController/Data/{}'.format(fileName2))
# x_values_1 = []
# y_values_1 = []
# x_values_2 = []
# y_values_2 = []
# index = 0
# while index < 480:
#     x_values_1.append(data1['Temperature'][index:index + 9].mean())
#     y_values_1.append(data1['Resistances'][index:index + 9].mean())
#     x_values_2.append(data2['Temperature'][index:index + 9].mean())
#     y_values_2.append(data2['Resistances'][index:index + 9].mean())
#     index += 10

# plt.plot(x_values_1, y_values_1, label='Front')
# plt.plot(x_values_2, y_values_2, label="Rear")
# plt.xlabel("Temperatures(Kelvin)")
# plt.ylabel("Resistances")
# plt.legend()
# plt.show()

fileName = "resistance_lockin.csv"
data1 = pd.read_csv('D:/CINTRA/kappa/LakeShore330TemperatureController/{}'.format(fileName))
x_values = []
y_values = []
index = 0
while index < 480:
    x_values.append(data1['Temperature'][index:index + 9].mean())
    y_values.append(data1['X'][index:index + 9].mean() / data1['Current'][index:index + 9].mean())
    index += 10
temp1 = data1["Temperature"][20:29].mean()
temp2 = data1["Temperature"][-10:-1].mean()
resistance1 = data1['X'][20:29].mean() / data1['Current'][20:29].mean()
resistance2 = data1['X'][-10:-1].mean() / data1['Current'][-10:-1].mean()
TCR = (resistance2 - resistance1)/ ((temp2 - temp1) * 16.1)
print(TCR)
plt.text(100, 5, "TCR: {}".format(TCR))
plt.plot(x_values, y_values,)
plt.xlabel("Temperatures(Kelvin)")
plt.ylabel("Resistances")
plt.show()