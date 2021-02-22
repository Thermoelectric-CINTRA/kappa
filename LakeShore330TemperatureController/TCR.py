import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import datetime

fileName = "resistance_10K_to_475K.csv"
data = pd.read_csv('D:/CINTRA/kappa/LakeShore330TemperatureController/Data/{}'.format(fileName))
x_values = []
y_values = []
index = 0
while index < 480:
    x_values.append(data['Temperature'][index:index + 9].mean())
    y_values.append(data['Resistances'][index:index + 9].mean())
    index += 10
print(x_values, y_values)

plt.plot(x_values, y_values)
plt.xlabel("Temperatures(Kelvin)")
plt.ylabel("Resistances")
plt.show()