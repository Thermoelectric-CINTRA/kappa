from pymeasure.instruments.keithley import Keithley2400
import time
import pandas as pd
import csv
import os, os.path
import datetime
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
data_points = 3

dataframe = {"Timestamp", "Temperautre", "Resistance", "Mean", "Std"}
df = pd.DataFrame(dataframe)

while count < data_points:
    data_1 = pd.DataFrame({
        "Timestamp": count,
        "Temperautre": Temp,
        "Resistance": keithley.resistance
    })
    df = df.append(data_1, ignore_index=False)
    count += 1
    time.sleep(1)
    print(df)

df.to_csv(fileName, mode="a")