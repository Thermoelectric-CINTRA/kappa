import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import datetime

fileName1 = "resistance_front.csv"
fileName2 = "resistance_rear.csv"
data1 = pd.read_csv('D:/CINTRA/kappa/LakeShore330TemperatureController/Data/{}'.format(fileName1))
data2 = pd.read_csv('D:/CINTRA/kappa/LakeShore330TemperatureController/Data/{}'.format(fileName2))
x_values_1 = []
y_values_1 = []
x_values_2 = []
y_values_2 = []
index = 0
while index < 480:
    x_values_1.append(data1['Temperature'][index:index + 9].mean())
    y_values_1.append(data1['Resistances'][index:index + 9].mean())
    x_values_2.append(data2['Temperature'][index:index + 9].mean())
    y_values_2.append(data2['Resistances'][index:index + 9].mean())
    index += 10
# print(x_values, y_values)

plt.plot(x_values_1, y_values_1, label='Front')
plt.plot(x_values_2, y_values_2, label="Rear")
plt.xlabel("Temperatures(Kelvin)")
plt.ylabel("Resistances")
plt.legend()
plt.show()