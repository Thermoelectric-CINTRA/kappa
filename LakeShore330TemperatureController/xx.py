# python_live_plot.py

import random
from itertools import count
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

plt.style.use('fivethirtyeight')

x_values = []
y_values = []

index = count()

def animate(self):
    data = pd.read_csv('D:/CINTRA/kappa/LakeShore330TemperatureController/Data/temperature.csv')
    x_values = data['Time']
    y_values = data['Temperature']
    plt.cla()
    plt.plot(x_values, y_values)
    plt.xlabel('Time')
    plt.ylabel('Temperature')
    plt.title('LakeShore330')
    plt.gcf().autofmt_xdate()
    plt.tight_layout()

ani = FuncAnimation(plt.gcf(), animate, 1000)

plt.tight_layout()
plt.show()