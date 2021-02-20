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

def RecordKelvin():
    temperatureController = LakeShore330("GPIB0::5")
    second = 0
    date = datetime.date.today()
    DIR = 'Data'
    fileNum = len([name for name in os.listdir(DIR) if os.path.isfile(os.path.join(DIR, name))])
    fileName = "Data/temperature_{}_{}.csv".format(date, fileNum)
    
    firstpointcounter = 0
    while firstpointcounter < 10:
        time.sleep(1)
        FirstPoint(temperatureController.temperature_A, firstpointcounter)
        firstpointcounter += 1
    
    setpoint = 10
    temperatureController.setpoint = setpoint
    temperatureController.heater_range = "low"
    step = 50
    hold_time = 0

    # temperatureController.auto_tune = "PID"
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

        if setpoint >= temperature - 0.3 and setpoint <= temperature + 0.3:
            hold_time += 1
            print("Hold time of {}K in second: {}".format(temperature, hold_time))
            if hold_time >= 60:
                RecordOhm(temperature)
                time.sleep(1)
                setpoint += step
                temperatureController.setpoint = setpoint
                # if setpoint < 50:
                #     temperatureController.heater_range = "medium"
                # # elif setpoint >= 50 and setpoint <= 250:
                # #     temperatureController.heater_range = "medium"
                # else:
                # temperatureController.heater_range = "high"
                print("Changing to new setting point: {}".format(setpoint))
                
        else:
            hold_time = 0
            print("Hold time clear")

    csvfile.close()

def LivePlot():
    time.sleep(50)
    def animate(self):
        date = datetime.date.today()
        DIR = 'Data'
        fileNum = len([name for name in os.listdir(DIR) if os.path.isfile(os.path.join(DIR, name))]) - 1
        fileName = "temperature_{}_{}.csv".format(date, fileNum)
        data = pd.read_csv('Data/{}'.format(fileName))
        x_values = data['Timestamp']
        y_values = data['Temperatures']
        setpoint_values = data['SetPoints']
        plt.cla()
        
        if x_values[len(x_values)-1] > 60 and x_values[len(x_values)-1] < 3600 :
            plt.xlabel('Time(minutes)')
            plt.plot(x_values/60, y_values)
            plt.plot(x_values/60, setpoint_values)
            plt.plot(x_values/60, setpoint_values+0.3)
            plt.plot(x_values/60, setpoint_values-0.3)

        elif x_values[len(x_values)-1] > 3600 :
            plt.xlabel('Time(hours)')
            plt.plot(x_values/3600, y_values)
            plt.plot(x_values/60, setpoint_values)
            plt.plot(x_values/3600, setpoint_values+0.3)
            plt.plot(x_values/3600, setpoint_values-0.3)
        else:
            plt.xlabel('Time(seconds)')
            plt.plot(x_values, y_values)
            plt.plot(x_values, setpoint_values)
            plt.plot(x_values, setpoint_values+0.3)
            plt.plot(x_values, setpoint_values-0.3)
        
        plt.ylabel('Temperatures(Kelvin)')
        plt.title('LakeShore330 Temperature Controller')
        plt.gcf().autofmt_xdate()
        plt.tight_layout()
    time.sleep(0.1)
    ani = FuncAnimation(plt.gcf(), animate, 1000)

    plt.tight_layout()
    plt.show()

def RecordOhm(temp):
    print("Start record resistance.")
    keithley = Keithley2400("GPIB0::6")
    keithley.reset()
    keithley.measure_resistance()
    keithley.wires = 4
    keithley.resistance_nplc = 10
    keithley.enable_source()

    fileName = "Data/resistance_10K_to_475K.csv"

    Temp = temp
    count = 0
    datapoints = 10
    second = 0

    while count < datapoints:
        time.sleep(0.1)
        print(keithley.resistance)
        count += 1

        with open(fileName, 'a', newline='') as csvfile:
            header = ["Timestamp", "Temperature",  "Resistances", "Mean", "Std"]
            writer = csv.DictWriter(csvfile, fieldnames=header)
            if csvfile.tell() == 0:
                writer.writeheader()
            writer.writerow(
                {
                    "Timestamp": second,
                    "Temperature": Temp,
                    "Resistances": keithley.resistance
                }
            )
            second += 1
        csvfile.close()

def FirstPoint(temp, time):
    print("Start record first point resistance.")
    keithley = Keithley2400("GPIB0::6")
    keithley.reset()
    keithley.measure_resistance()
    keithley.wires = 4
    keithley.resistance_nplc = 10
    keithley.enable_source()

    fileName = "Data/resistance_10K_to_475K.csv"

    Temp = temp
    second = time

    with open(fileName, 'a', newline='') as csvfile:
        header = ["Timestamp", "Temperature",  "Resistances", "Mean", "Std"]
        writer = csv.DictWriter(csvfile, fieldnames=header)
        if csvfile.tell() == 0:
            writer.writeheader()
        writer.writerow(
            {
                "Timestamp": second,
                "Temperature": Temp,
                "Resistances": keithley.resistance
            }
        )
    csvfile.close()

def main():
    P1 = Process(target=RecordKelvin)
    P2 = Process(target=LivePlot)
    P1.start()
    P2.start()
    P1.join()
    P2.join()

if __name__ == "__main__":
    main()