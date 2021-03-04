import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import datetime

fileName1 = "resistance_10K_to_475K.csv"
# fileName2 = "resistance_rear.csv"
data1 = pd.read_csv('D:/CINTRA/kappa/LakeShore330TemperatureController/Data/{}'.format(fileName1))
# data2 = pd.read_csv('D:/CINTRA/kappa/LakeShore330TemperatureController/Data/{}'.format(fileName2))
x_values_1 = []
y_values_1 = []
# x_values_2 = []
# y_values_2 = []
index = 0
while index < 480:
    x_values_1.append(data1['Temperature'][index:index + 9].mean())
    y_values_1.append(data1['Resistances'][index:index + 9].mean())
#     x_values_2.append(data2['Temperature'][index:index + 9].mean())
#     y_values_2.append(data2['Resistances'][index:index + 9].mean())
    index += 10

plt.plot(x_values_1, y_values_1, label='DC')
# plt.plot(x_values_2, y_values_2, label="Rear")
# plt.xlabel("Temperatures(Kelvin)")
# plt.ylabel("Resistances")

# plt.show()

fileName2 = "resistance_lockin.csv"
data2 = pd.read_csv('D:/CINTRA/kappa/LakeShore330TemperatureController/{}'.format(fileName2))
x_values_2 = []
y_values_2 = []
index = 0
while index < 480:
    x_values_2.append(data2['Temperature'][index:index + 9].mean())
    y_values_2.append(data2['X'][index:index + 9].mean() / data2['Current'][index:index + 9].mean())
    index += 10
temp1 = data2["Temperature"][20:29].mean()
temp2 = data2["Temperature"][-10:-1].mean()
resistance1 = data2['X'][20:29].mean() / data2['Current'][20:29].mean()
resistance2 = data2['X'][-10:-1].mean() / data2['Current'][-10:-1].mean()
TCR_AC = (resistance2 - resistance1)/ ((temp2 - temp1) * 16.1)
temp3 = data1["Temperature"][20:29].mean()
temp4 = data1["Temperature"][-10:-1].mean()
resistance3 = data1["Resistances"][20:29].mean()
resistance4 = data1["Resistances"][-10:-1].mean()
TCR_DC = (resistance4 - resistance3) / ((temp4 - temp3) * 16.1)
plt.text(100, 5, "TCR_AC: {}".format(TCR_AC))
plt.text(200, 8, "TCR_DC: {}".format(TCR_DC))
plt.plot(x_values_2, y_values_2, label="AC")
plt.xlabel("Temperatures(Kelvin)")
plt.ylabel("Resistances")
plt.legend()
plt.show()