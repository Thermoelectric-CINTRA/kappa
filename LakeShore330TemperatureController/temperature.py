from pymeasure.instruments.lakeshore import LakeShore331
import time
import matplotlib as plt
import csv

import pandas as pd
import matplotlib.pyplot as plt
from itertools import count
from matplotlib.animation import FuncAnimation

# plt.style.use('fivethirtyeight')

# x_values = []
# y_values = []

# index = count()

# def animate(self):
#     data = pd.read_csv('Data/temperature.csv')
#     x_values = data['Time']
#     y_values = data['Temperature']
#     plt.cla()
#     plt.plot(x_values, y_values)
#     plt.xlabel('Time')
#     plt.ylabel('Temperature')
#     plt.title('LakeShore330')
#     plt.gcf().autofmt_xdate()
#     plt.tight_layout()

temperatureController = LakeShore331("GPIB0::5")
countX = 0
while temperatureController.temperature_A < 320:
    temperature = temperatureController.temperature_A
    print(temperature)
    with open('Data/temperature.csv', 'a', newline='') as csvfile:
        header = ["Time", "Temperature"]
        writer = csv.DictWriter(csvfile, fieldnames=header)
        if csvfile.tell() == 0:
            writer.writeheader()
        writer.writerow(
            {
                "Time": countX,
                "Temperature": temperature
            }
        )
    countX += 1
    time.sleep(1)

csvfile.close()

# ani = FuncAnimation(plt.gcf(), animate, 1000)
# plt.tight_layout()
# plt.show()

