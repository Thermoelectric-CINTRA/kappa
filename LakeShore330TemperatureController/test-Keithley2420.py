from pymeasure.instruments.keithley import Keithley2420
import time

keithley = Keithley2420("GPIB0::6")
keithley.config_measurement = "Ohms"
# keithley.count = 100
keithley.buffer_points = 1
keithley.initiate()
# print(keithley.config_measurement)
# # print(keithley.count)
# time.sleep(1)
# keithley.abort()
keithley.is_buffer_full
DATA = keithley.get_data()
print(DATA)