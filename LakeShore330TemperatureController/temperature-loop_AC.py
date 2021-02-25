from pymeasure.instruments.lakeshore import LakeShore330
from pymeasure.instruments.keithley import Keithley2400
from pymeasure.instruments.hp import HP34401A
from pymeasure.instruments.keysight import Keysight33210A
from pymeasure.instruments.nf import LI5660

import csv
import datetime
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from multiprocessing import Process
import os, os.path
from datetime import datetime as dt
import time

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
        elif setpoint > 20:
            temperatureController.heater_range = "high"
            temperatureController.auto_tune = "PID"
        else:
            temperatureController.heater_range = "off"

    setpoint = 70
    endpoint = 474.9
    temperatureController.setpoint = setpoint
    PID(setpoint)
    step = 10
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

        if setpoint >= temperature - 0.2 and setpoint <= temperature + 0.2:
            hold_time += 1
            print("Hold time of {}K in second: {}".format(temperature, hold_time))
            if hold_time >= 120:
                ohmcounter_front = 0
                while ohmcounter_front < 10:
                    now = dt.now().time()
                    RecordOhm(temperatureController.temperature_A, now)
                    ohmcounter_front += 1
                time.sleep(1)
                print("P: {}, I: {}, D: {}".format(temperatureController.gain, temperatureController.reset, temperatureController.rate))
                setpoint += step
                if setpoint > endpoint:
                    temperatureController.heater_range = "off"
                    print("Measurement Done.")
                    break
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

def RecordOhm(temp, Timestamp):
    print("Start Recording.")
    # NF Lock In
    nf = LI5660("GPIB0::1")
    # Function Generator
    keysight = Keysight33210A("GPIB0::4")
    # Current Meter
    hp = HP34401A("GPIB0::2")
    # points = 20
    # Recording 1W data
    nf.clear_all_buffer()
    # phaseshift = nf.fetch       # Get the phase shift after setting the new internal oscillationg frequency
    nf.data_feed("Buffer1",30)
    nf.data_feed_control("Buffer1", "Always")
    nf.data_points("Buffer1")
    nf.source_trigger("Bus")
    # theta -= phaseshift[1]
    # nf.primary_phase_shift(0)     # Counter the phase shift
    nf.delay(0)
    nf.initiate()
    print("Operation condition: ", nf.status_operation_condition)
    # time.sleep(1)
    nf.trigger()

    # while nf.status_operation_condition < 256:
    #     # print(nf.status_operation_condition)
    #     # print(nf.buffer1_count, "/{}".format(points))
    #     print("NF Status: ", nf.status_operation_condition)
    # time.sleep(1)
    data_buffer = nf.get_buffer("Buffer1", 1, 0)
    nf.abort()
    current = hp.current_ac
    vin = keysight.amplitude
    time.sleep(1)
    fileName = "resistance_lockin.csv"
    with open(fileName, 'a', newline='') as csvfile:
        header = ["Timestamp", "Temperature", "R", "Theta", "X", "Y", "Current", "Vin"]
        writer = csv.DictWriter(csvfile, fieldnames=header)
        if csvfile.tell() == 0:
            writer.writeheader()
        writer.writerow(
            {
                "Timestamp": Timestamp,
                "Temperature": temp,
                "R": data_buffer[0],
                "Theta": data_buffer[1],
                "X": data_buffer[2],
                "Y": data_buffer[3],
                "Current": current,
                "Vin": vin
            }
        )
    csvfile.close()

def main():
    P1 = Process(target=TempLoop)
    P2 = Process(target=LivePlot)
    P1.start()
    P2.start()
    P1.join()
    P2.join()

if __name__ == "__main__":
    main()