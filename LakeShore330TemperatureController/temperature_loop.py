from pymeasure.instruments.lakeshore import LakeShore331
from pymeasure.instruments.keysight import Keysight33210A

import time
import csv
import datetime
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from multiprocessing import Process
import os, os.path

def RecordKelvin():
    temperatureController = LakeShore331("GPIB0::5")
    second = 0
    date = datetime.date.today()
    DIR = 'Data'
    fileNum = len([name for name in os.listdir(DIR) if os.path.isfile(os.path.join(DIR, name))]) + 1
    fileName = "Data/temperature_{}_{}.csv".format(date, fileNum)
    print(date)
    while True:
        temperature = temperatureController.temperature_A

        with open(fileName, 'a', newline='') as csvfile:
            header = ["Timestamp", "Temperatures"]
            writer = csv.DictWriter(csvfile, fieldnames=header)
            if csvfile.tell() == 0:
                writer.writeheader()
            writer.writerow(
                {
                    "Timestamp": second,
                    "Temperatures": temperature
                }
            )
        second += 1
        time.sleep(1)

    csvfile.close()

def LivePlot():
    def animate(self):
        date = datetime.date.today()
        DIR = 'Data'
        fileNum = len([name for name in os.listdir(DIR) if os.path.isfile(os.path.join(DIR, name))])
        fileName = "temperature_{}_{}.csv".format(date, fileNum)
        data = pd.read_csv('Data/{}'.format(fileName))
        x_values = data['Timestamp']
        y_values = data['Temperatures']
        plt.cla()
        
        if x_values[len(x_values)-1] > 60 and x_values[len(x_values)-1] < 3600 :
            plt.xlabel('Time(minutes)')
            plt.plot(x_values/60, y_values)
        elif x_values[len(x_values)-1] > 3600 :
            plt.xlabel('Time(hours)')
            plt.plot(x_values/3600, y_values)
        else:
            plt.xlabel('Time(seconds)')
            plt.plot(x_values, y_values)
        
        plt.ylabel('Temperatures(Kelvin)')
        plt.title('LakeShore330 Temperature Controller')
        plt.gcf().autofmt_xdate()
        plt.tight_layout()
    time.sleep(0.1)
    ani = FuncAnimation(plt.gcf(), animate, 1000)

    plt.tight_layout()
    plt.show()

def main():
    P1 = Process(target=RecordKelvin)
    P2 = Process(target=LivePlot)
    P1.start()
    P2.start()
    P1.join()
    P2.join()

if __name__ == "__main__":
    main()