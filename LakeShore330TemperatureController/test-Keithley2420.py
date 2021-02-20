from pymeasure.instruments.keithley import Keithley2420

keithley = Keithley2420("GPIB0::6")
# keithley.config_measurement = "Ohms"
# keithley.count = 100
keithley.initiate()
print(keithley.config_measurement)
# print(keithley.count)