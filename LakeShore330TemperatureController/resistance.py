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
# date = datetime.date.today()
# DIR = 'Data'
# fileNum = len([name for name in os.listdir(DIR) if os.path.isfile(os.path.join(DIR, name))]) + 1
# fileName = "Data/resistance_{}_{}.csv".format(date, fileNum)
fileName = "Data/resistance.csv"

Temp = 330
count = 0
second = 0
while count < 10:
    time.sleep(1)
    print(keithley.resistance)
    count += 1

    with open(fileName, 'a', newline='') as csvfile:
        header = ["Timestamp", "Temperature",  "Resistances", "Mean","Std"]
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

# df = pd.read_csv(fileName)
# q1 = """SELECT Resistances FROM df WHERE Temperature = {} """.format(Temp)
# # df["Mean"] = df.Resistances.mean()
# # df["Std"] = df.Resistances.std()
# print(type(ps.sqldf(q1, locals())))

# df["Mean"] = np.average(ps.sqldf(q1, locals()))
# df.to_csv(fileName, index=False)

# q2 = """SELECT Mean FROM df WHERE Temperature = {} """.format(Temp)
# df["Std"] = np.std(ps.sqldf(q2, locals()))
# df.to_csv(fileName, index=False)
# print(df)

# update = pd.DataFrame([mean, std],columns=["Mean", 'Std'])

# resistances = ps.sqldf(q1, locals()).mean()
# print(resistances)
