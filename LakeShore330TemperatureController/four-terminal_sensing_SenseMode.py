# Import necessary packages
from pymeasure.instruments.keithley import Keithley2400
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from time import sleep
"""
Example Four-terminal sensing (Vierleitermessung) with one channel

First 2-wire measurement with Channel A -> R_I + R_M are measured
Than 4-wire measurement with Channel A Sense-wire R_M is measured


     -------------------------------
     |                             |
    |-|              --------------°
    | | R_I          |             |
    |-|              |            |-|
     |               |            | | R_M
  ------- SMU_A   ------- SMU_A   |-|
  |  A  | voltage | A_S | Sense    |
  ------- source  ------- wires    |
     |               |             |
     ----------------°--------------

A...   SMU Channel A voltage source
A_S... SMU Channel A sense wires for the measurement of R_M only used in 4-wire mode
R_M... Resistor that you want to measure
R_I... Resistor that interferes with the direct measurement of R_M in 2-wire mode

In this example the R_I is simulating possible lead and contact resistances, that are interfering with a direct 
measurement of R_M. Using the Four-terminal sensing (Vierleitermessung) with the 4-wire mode the lead and contact 
resistances are ignored and only the R_M is measured. This setup is used for electrical resistance measurements in 
which the resistor that is measured has a resistance in the range of the lead and contact resistances or when a very 
precise measurement is necessary.

The 2-wire measurement will measure the series circuit of R_M + R_I (+ lead and contact resistances)
The 4-wire measurement will measure the R_M

"""

# Connect to the Sourcemeter
sourcemeter = Keithley2400("GPIB0::5")  #using RS 232 COM6

# Select the channel that is connected
#smu = sm.get_channel(sm.CHANNEL_A)
#smu = sm.get_channel(sm.CHANNEL_B)

""" Define the current for both measurements. The current limit for all measurements is 10*current."""
""" The current has to be so low that the measured voltage is less than 20 V!!!!"""

current = 1e-5
R2wire = []
#R2wire_cvoltage = []
#R4wire = []
current2wire = []
voltage2wire = []

sourcemeter.source_current = current
# Allocate arrays to store the measurement results
current2wire = np.zeros_like(0, 5)
voltage2wire = np.zeros_like(0, 5)

sourcemeter.measure_voltage()
sourcemeter.apply_current()

for i in range(0, 5):
    """ Configure Channel A for a 2-wire measurement """
    # reset to default settings
    sourcemeter.reset()
    # set the sense mode to local (2-wire) - this is not necessary if you reset the channel previously
    #sourcemeter.wires = 2
    # setup the operation mode and what will be shown at the display
    #sourcemeter.enable_source()
    #sourcemeter.apply_current()
    #sleep(0.1)
    #sourcemeter.resistance()
    # define the initial parameters for Channel A
    #sourcemeter.voltage_range = 5
    #sourcemeter.compliance_voltage = 5
    #sourcemeter.apply_voltage = 0
    # sourcemeter.source_current_range = current*10
    # sourcemeter.compliance_current = current*10
    #sourcemeter.apply_current = current

    """ Do the 2-wire measurement """
    # enable the outputs
    sourcemeter.enable_source()
    sourcemeter.start_buffer()
    # set the current
    # measure the current and the voltage
    #sourcemeter.measure_current()
    sleep(0.1)
    current2wire = sourcemeter.measure_current()
    #sourcemeter.source_current = current2wire[i]
    sleep(0.1)
    sourcemeter.measure_voltage()
    voltage2wire[i] = sourcemeter.voltage
    # disable the outputs
    sourcemeter.disable_source()

#------------------------------------------------------------------------------------
    #
    # """ Configure Channel A for a 2-wire measurement with constant voltage """
    #
    # # reset to default settings
    # sourcemeter.reset()
    #
    # # set the sense mode to local (2-wire) - this is not necessary if you reset the channel previously
    # #smu.set_sense_2wire()
    #
    # # setup the operation mode and what will be shown at the display
    # sourcemeter.source_voltage = 1
    # sourcemeter.measure_resistance()
    #
    # # define the initial parameters for Channel A
    # #sourcemeter.voltage_range = 5
    # #sourcemeter.compliance_voltage = 5
    # sourcemeter.source_voltage = 0
    # sourcemeter.source_current_range = current*10
    # sourcemeter.compliance_current = current*10
    # sourcemeter.source_current = 0
    #
    # """ Do the 2-wire measurement by applying constant voltage """
    #
    # # enable the outputs
    # sourcemeter.enable_source()
    #
    # # set the voltage
    # sourcemeter.source_voltage = 1
    #
    # # measure the current and the voltage
    # current2wire_cvoltage = sourcemeter.measure_current()
    # voltage2wire_cvoltage = sourcemeter.measure_voltage()
    #
    # # disable the outputs
    # sourcemeter.disable_source()

#-----------------------------------------------------------------------------------
    #
    # """ Configure Channel A for a 4-wire measurement """
    # # reset to default settings
    # sourcemeter.reset()
    #
    # # setup the operation mode and what will be shown at the display
    # sourcemeter.source_current = 1
    # sourcemeter.measure_resistance()
    #
    # # set the sense mode to remote (4-wire)
    # sourcemeter.wire = 4
    #
    # # define the initial parameters for Channel A
    # #sourcemeter.voltage_range = 5
    # #sourcemeter.compliance_voltage = 5
    # sourcemeter.apply_voltage = 0
    # sourcemeter.current_range = current*10
    # sourcemeter.compliance_current = current*10
    # sourcemeter.apply_current = 0
    #
    # """ Do the 4-wire measurement """
    #
    # # enable the outputs
    # sourcemeter.enable_source()
    #
    # # set the current
    # #smu.set_current(current*(i%2))
    # sourcemeter.apply_voltage = current
    # # measure the current and the voltage
    # current4wire = sourcemeter.measure_current()
    # voltage4wire = sourcemeter.measure_voltage()
    #
    # # disable the outputs
    # sourcemeter.disable_source()

    """ Calculate and display the Measurement """

    R2wire.append(voltage2wire/current2wire)
    #R2wire_cvoltage.append(voltage2wire_cvoltage/current2wire_cvoltage)
    #R4wire.append(voltage4wire/current4wire)
    print("Cycle: " + str(i))
    print("Voltage 2-Wire = " + str(voltage2wire) + ". Current 2-Wire = " + str(current2wire))
    #print("Voltage 2-Wire Const. Voltage = " + str(voltage2wire_cvoltage) + ". Current 2-Wire = " + str(current2wire_cvoltage))
    #print("Voltage 4-Wire = " + str(voltage4wire) + ". Current 4-Wire = " + str(current4wire))

    print("The resistance measured with the 2-wire mode is " + str(R2wire[i]) + "Ohms")
    #print("The resistance measured with the 2-wire mode with constant voltage is " + str(R2wire_cvoltage[i]/1e6) + "MOhm")
    #print("The resistance measured with the 4-wire mode is " + str(R4wire[i]/1e6) + "MOhm")

print("\n\n\nResistance 2-wire mode ="+str(np.mean(R2wire))+"+/-"+str(np.std(R2wire))+"Ohms")
#print("Resistance 2-wire mode with constant voltage ="+str(numpy.mean(R2wire_cvoltage)/1e6)+"+/-"+str(numpy.std(R2wire_cvoltage)/1e6)+"MOhm")
#print("Resistance 4-wire mode ="+str(numpy.mean(R4wire)/1e6)+"+/-"+str(numpy.std(R4wire)/1e6)+"MOhm")

""" Disconnect from the SMU """

# reset the SMU
sourcemeter.reset()

# disconnect from the SMU
sourcemeter.shutdown()
