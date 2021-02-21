from pymeasure.instruments.lakeshore import LakeShore330
from pymeasure.instruments.keithley import Keithley2400

import time
import csv
import datetime
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from multiprocessing import Process
import os, os.path

def TempLoop():
    temperatureController = LakeShore330("GPIB0::5")
    second = 0
    date = datetime.date.today()
    DIR = 'Data/{}'.format(date)
    try:
        os.mkdir(DIR)
    except OSError:
        print ("Creation of the directory %s failed" % DIR)
    else:
        print ("Successfully created the directory %s " % DIR)
    time.sleep(0.1)
    fileNum = len([name for name in os.listdir(DIR) if os.path.isfile(os.path.join(DIR, name))]) + 1
    fileName = "Data/{}/temperature_{}.csv".format(date, fileNum)

    def PID(setpoint):
        if setpoint <= 10:
            temperatureController.gain = 5
            temperatureController.reset = 500
            temperatureController.rate = 0
            temperatureController.heater_range = "medium"
        elif setpoint <= 15 and setpoint > 10:
            temperatureController.gain = 50
            temperatureController.reset = 500
            temperatureController.rate = 0
            temperatureController.heater_range = "medium"
        elif setpoint <= 20 and setpoint > 15:
            temperatureController.gain = 1
            temperatureController.reset = 900
            temperatureController.rate = 0
            temperatureController.heater_range = "high"
        elif setpoint <= 25 and setpoint > 20:
            temperatureController.gain = 1
            temperatureController.reset = 100
            temperatureController.rate = 0
            temperatureController.heater_range = "high"
        # elif setpoint <= 60 and setpoint > 45:
        #     temperatureController.gain =3
        #     temperatureController.reset = 900
        #     temperatureController.rate = 200
        #     temperatureController.heater_range = "high"
        # elif setpoint <= 75 and setpoint > 60:
        #     temperatureController.gain = 15
        #     temperatureController.reset = 900
        #     temperatureController.rate = 200
        #     temperatureController.heater_range = "high"
        # elif setpoint <= 90 and setpoint > 75:
        #     temperatureController.gain = 20
        #     temperatureController.reset = 900
        #     temperatureController.rate = 0
        #     temperatureController.heater_range = "high"
        # elif setpoint <= 105 and setpoint > 90:
        #     temperatureController.gain = 30
        #     temperatureController.reset = 900
        #     temperatureController.rate = 200
        #     temperatureController.heater_range = "high"
        # elif setpoint <= 120 and setpoint > 105:
        #     temperatureController.gain = 40
        #     temperatureController.reset = 900
        #     temperatureController.rate = 200
        #     temperatureController.heater_range = "high"
        # elif setpoint <= 135 and setpoint > 120:
        #     temperatureController.gain = 50
        #     temperatureController.reset = 900
        #     temperatureController.rate = 200
        #     temperatureController.heater_range = "high"
        # elif setpoint <= 150 and setpoint > 135:
        #     temperatureController.gain = 60
        #     temperatureController.reset = 900
        #     temperatureController.rate = 200
        #     temperatureController.heater_range = "high"
        # elif setpoint <= 165 and setpoint > 150:
        #     temperatureController.gain = 70
        #     temperatureController.reset = 900
        #     temperatureController.rate = 200
        #     temperatureController.heater_range = "high"
        # elif setpoint <= 180 and setpoint > 165:
        #     temperatureController.gain = 80
        #     temperatureController.reset = 900
        #     temperatureController.rate = 200
        #     temperatureController.heater_range = "high"
        # elif setpoint <= 195 and setpoint > 180:
        #     temperatureController.gain = 90
        #     temperatureController.reset = 900
        #     temperatureController.rate = 200
        #     temperatureController.heater_range = "high"
        # elif setpoint <= 210 and setpoint > 195:
        #     temperatureController.gain = 100
        #     temperatureController.reset = 900
        #     temperatureController.rate = 200
        #     temperatureController.heater_range = "high"
        # elif setpoint <= 225 and setpoint > 210:
        #     temperatureController.gain = 110
        #     temperatureController.reset = 900
        #     temperatureController.rate = 200
        #     temperatureController.heater_range = "high"
        # elif setpoint <= 240 and setpoint > 225:
        #     temperatureController.gain = 120
        #     temperatureController.reset = 900
        #     temperatureController.rate = 200
        #     temperatureController.heater_range = "high"
        # elif setpoint <= 255 and setpoint > 240:
        #     temperatureController.gain = 130
        #     temperatureController.reset = 900
        #     temperatureController.rate = 200
        #     temperatureController.heater_range = "high"
        # elif setpoint <= 270 and setpoint > 255:
        #     temperatureController.gain = 140
        #     temperatureController.reset = 900
        #     temperatureController.rate = 200
        #     temperatureController.heater_range = "high"
        # elif setpoint <= 285 and setpoint > 270:
        #     temperatureController.gain = 150
        #     temperatureController.reset = 900
        #     temperatureController.rate = 200
        #     temperatureController.heater_range = "high"
        # elif setpoint <= 300 and setpoint > 285:
        #     temperatureController.gain = 160
        #     temperatureController.reset = 900
        #     temperatureController.rate = 200
        #     temperatureController.heater_range = "high"
        else:
            temperatureController.heater_range = "off"

    setpoint = 15
    temperatureController.setpoint = setpoint
    PID(setpoint)
    step = 5
    hold_time = 0

    while True:
        temperature = temperatureController.temperature_A

        with open(fileName, 'a', newline='') as csvfile:
            header = ["Timestamp", "Temperatures", "SetPoints"]
            writer = csv.DictWriter(csvfile, fieldnames=header)
            if csvfile.tell() == 0:
                writer.writeheader()
            writer.writerow(
                {
                    "Timestamp": second,
                    "Temperatures": temperature,
                    "SetPoints": setpoint
                }
            )
        second += 1
        time.sleep(1)

        if setpoint >= temperature - 0.1 and setpoint <= temperature + 0.1:
            hold_time += 1
            print("Hold time of {}K in second: {}".format(temperature, hold_time))
            if hold_time >= 60:
                # RecordOhm(temperature)
                time.sleep(1)
                setpoint += step
                temperatureController.setpoint = setpoint
                PID(setpoint)
                print("Changing to new setting point: {}".format(setpoint))
                
        else:
            hold_time = 0
            print("Hold time clear")

    csvfile.close()

def LivePlot():
    time.sleep(1)
    def animate(self):
        date = datetime.date.today()
        DIR = 'Data/{}'.format(date)
        fileNum = len([name for name in os.listdir(DIR) if os.path.isfile(os.path.join(DIR, name))])
        fileName = "Data/{}/temperature_{}.csv".format(date, fileNum)
        data = pd.read_csv(fileName)
        x_values = data['Timestamp']
        y_values = data['Temperatures']
        setpoint_values = data['SetPoints']
        plt.cla()
        
        if x_values[len(x_values)-1] > 60 and x_values[len(x_values)-1] < 3600 :
            plt.xlabel('Time(minutes)')
            plt.plot(x_values/60, y_values)
            plt.plot(x_values/60, setpoint_values)
            plt.plot(x_values/60, setpoint_values+0.1)
            plt.plot(x_values/60, setpoint_values-0.1)

        elif x_values[len(x_values)-1] > 3600 :
            plt.xlabel('Time(hours)')
            plt.plot(x_values/3600, y_values)
            plt.plot(x_values/3600, setpoint_values)
            plt.plot(x_values/3600, setpoint_values+0.1)
            plt.plot(x_values/3600, setpoint_values-0.1)
        else:
            plt.xlabel('Time(seconds)')
            plt.plot(x_values, y_values)
            plt.plot(x_values, setpoint_values)
            plt.plot(x_values, setpoint_values+0.1)
            plt.plot(x_values, setpoint_values-0.1)
        
        plt.ylabel('Temperatures(Kelvin)')
        plt.title('LakeShore330 Temperature Controller')
        plt.gcf().autofmt_xdate()
        plt.tight_layout()
    time.sleep(0.1)
    ani = FuncAnimation(plt.gcf(), animate, 1000)

    plt.tight_layout()
    plt.show()

def main():
    P1 = Process(target=TempLoop)
    P2 = Process(target=LivePlot)
    P1.start()
    P2.start()
    P1.join()
    P2.join()

if __name__ == "__main__":
    main()