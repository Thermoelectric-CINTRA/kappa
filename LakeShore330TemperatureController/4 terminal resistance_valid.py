#4 terminals resistance measurement - can choose 2 or 4 wires and the source current.
# Import necessary packages
from pymeasure.instruments.keithley import Keithley2400
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import time
from time import sleep
import datetime

now = datetime.datetime.now()

"""current sweep parameters"""
data_points = 6
# averages = 3
max_current = 0.001
min_current = -max_current
currents = np.linspace(min_current, max_current, num=data_points)

"""measurements arrays"""
Rwire = []
currentwire = []
voltagewire = []
spacer = []    # empty array to separate datasets
timecode = []
#cycles = [1,2,3]

""" Configure Channel A for a 2 or 4 -wire measurement """
mode = 4
# Connect to the Sourcemeter
sourcemeter = Keithley2400("GPIB0::6")  #using RS 232 COM6
sourcemeter.reset()
sourcemeter.use_front_terminals()
sourcemeter.wires = mode  # type 4 for 4 terminals measurement
sourcemeter.apply_current()
#sourcemeter.measure_resistance()
sourcemeter.enable_source()
#for cycle in range(1, 4):
for i in range(data_points):
        sourcemeter.source_current = currents[i]  # Sets the source current to min current mA

        """ Do the measurement """
        sourcemeter.measure_current()
        sleep(0.1)
        currentwire.append(sourcemeter.current)
        sleep(0.1)
        sourcemeter.measure_voltage()
        sleep(0.1)
        voltagewire.append(sourcemeter.voltage)
        sleep(0.1)
        Rwire.append(voltagewire[i]/currentwire[i])
        spacer.append(now.strftime("%H:%M:%S"))

"""add empty line at the end of the data"""
currentwire.append('\r')
voltagewire.append('\r')
Rwire.append('\r')
spacer.append('\r')

"""save data in.csv file"""
data = pd.DataFrame({
    # 'cycle is: ' + str(cycle): '',
    'Time': spacer,
    'Current (A)': currentwire,
    'Voltage (V)': voltagewire,
    'Resistance (Ohms) ' + str(mode) + 'wires': Rwire,
})

""" Disconnect from the SMU """
sourcemeter.shutdown()

data.to_csv("R_measurement_" + str(mode) + "wires_" + now.strftime("%Y-%m-%d") + ".csv", mode="a", index=False)



#
# for x in range(data_points):
#     """plot data"""
#     plt.plot(currentwire[x], voltagewire[x], '-b')
#     plt.ylabel('Voltage (mV)')
#     plt.xlabel('Current (mA)')
#     plt.title('I-V plot')
#     plt.show()

