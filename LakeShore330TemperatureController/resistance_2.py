from pymeasure.instruments.keithley import Keithley2400
import time
import pandas as pd
import csv
import os, os.path
from datetime import datetime
# import datetime
import matplotlib.pyplot as plt
import pandasql as ps
import numpy as np

keithley = Keithley2400("GPIB0::6")
keithley.reset()
keithley.measure_resistance()
keithley.wires = 4
keithley.enable_source()

fileName = "Data/resistance.csv"

Temp = 300
count = 0
datapoints = 10
second = 0
while count < datapoints:
    time.sleep(1)
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
    
    
Data = pd.read_csv(fileName)
print(Data)

mean_resistance = Data[["Temperature", "Resistances"]].groupby("Temperature").mean()
std_resistance = Data[["Temperature", "Resistances"]].groupby("Temperature").std()
Stats = Data[["Temperature", "Resistances"]].groupby("Temperature").describe()


print(mean_resistance)
print(std_resistance)
print(Stats)
# data = datetime.date.today()
time = datetime.now()
data_time = time.strftime("%m-%d-%Y-%H-%M-%S")
Stats.to_csv("R_measurements_{}.csv".format(data_time))
