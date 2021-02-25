from pymeasure.instruments.nf import LI5660
from pymeasure.instruments.keysight import Keysight33210A
from pymeasure.instruments.hp import HP34401A
from pymeasure.instruments.keithley import Keithley2000
import csv
import time
import os.path
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np 

theta = 0
points = 20
# voltage_sensitivitys = [10E-9, 20E-9, 50E-9, 100E-9, 200E-9, 500E-9,
#                         1E-6, 2E-6, 5E-6, 10E-6, 20E-6, 50E-6, 100E-6, 200E-6, 500E-6,
#                         1E-3, 2E-3, 5E-3, 10E-3, 20E-3, 50E-3, 100E-3, 200E-3, 500E-3,
#                         1]
nf = LI5660("GPIB0::1")
hp = HP34401A("GPIB0::2")
keithley = Keithley2000("GPIB0::3")
keysight = Keysight33210A("GPIB0::4")

nf.data1_format("Mlinear")      # R
nf.data2_format("Phase")        # Theta
nf.data3_format("Real")         # X
nf.data4_format("Imaginary")    # Y

# nf.reference_signal(source="Internal")
nf.coupling("AC")
nf.grounding("Ground") # Float or Ground
nf.input_terminal("AB")
nf.primary_harmonic("Off")

# nf.primary_phase_shift(theta)
nf.oscillator_amplitude(1)
nf.timer_state("On")
nf.interval(0.1)

HZ = 300        # Set start frequency equal to 100 Hz
endHz = 10E+3    # Set end frequency equal to 5000 Hz

# Recording 1W data
nf.clear_all_buffer()
# phaseshift = nf.fetch       # Get the phase shift after setting the new internal oscillationg frequency
nf.data_feed("Buffer1",30)
nf.data_feed_control("Buffer1", "Always")
nf.data_points("Buffer1",points)
nf.source_trigger("Bus")
# theta -= phaseshift[1]
# nf.primary_phase_shift(0)     # Counter the phase shift
nf.delay(0)
nf.initiate()
print("Operation condition: ", nf.status_operation_condition)
time.sleep(3)
nf.trigger()

while nf.status_operation_condition < 256:
    # print(nf.status_operation_condition)
    print(nf.buffer1_count, "/20")

data_buffer = nf.get_buffer("Buffer1", points, 0)
data1, data2, data3, data4 = 0, 0, 0, 0     # Reset data1, data2, data3, data4

with open("Data\/1w.csv", "w", newline="") as f:
    header = ["DATA 1", "DATA 2", "DATA 3", "DATA 4"]
    writer = csv.DictWriter(f, fieldnames=header)
    writer.writeheader()

    data = 0
    while data < len(data_buffer):
        writer.writerow({
            "DATA 1": data_buffer[data],
            "DATA 2": data_buffer[data+1],
            "DATA 3": data_buffer[data+2],
            "DATA 4": data_buffer[data+3]
        })
        data1 += data_buffer[data]
        data2 += data_buffer[data+1]
        data3 += data_buffer[data+2]
        data4 += data_buffer[data+3]
        data += 4
f.close()

with open("Data\/1st_Harmonic.csv", "a", newline='') as final:
    header2 = ["Frequency", "R", "Theta", "X", "Y"]
    writer = csv.DictWriter(final, fieldnames=header2)
    if final.tell() == 0:
        writer.writeheader()
    writer.writerow(
        {
            "Frequency": HZ,
            "R": data1/points,
            "Theta": data2/points,
            "X": data3/points,
            "Y": data4/points
        }
    )
final.close()

nf.notch_frequency(50)
nf.primary_notch_state("On")
nf.secondary_notch_state("On")

nf.primary_harmonic("On")
nf.primary_harmonic_multipliter(order=3)

# # Check the status
# status = nf.get_status()[0]
# voltage_sensitivity_level = nf.voltage_ac_range
# while status == 4:
nf.primary_voltage_sensitivity(2e-3)

while HZ <= endHz:
    # nf.primary_oscillator(HZ)     # Set the new nf frequency
    keysight.frequency = HZ         # Set the new keysight function generator frequency
    time.sleep(1)                   # python script sleep for 1 second, nf instrument need some time responce
    nf.clear_all_buffer()
    # phaseshift = nf.fetch         # Get the phase shift after setting the new internal oscillationg frequency
    nf.data_feed("Buffer1", 30)
    nf.data_feed_control("Buffer1","Always")
    nf.data_points("Buffer1",points)
    nf.source_trigger("Bus")
    # theta -= phaseshift[1]
    # nf.primary_phase_shift(0)       # Counter the phase shift
    nf.delay(0)
    nf.initiate()
    print("Operation condition: ", nf.status_operation_condition)
    time.sleep(3)
    nf.trigger()

    while nf.status_operation_condition < 256:
        # print(nf.status_operation_condition)
        print(nf.buffer1_count, "/20")

    data_buffer = nf.get_buffer("Buffer1", points, 0)
    data1, data2, data3, data4 = 0, 0, 0, 0     # Reset data1, data2, data3, data4
    finalfile = "Data\Final.csv"

    with open("Data\Recording_{}Hz.csv".format(HZ), "w", newline="") as f:
        header = ["DATA 1", "DATA 2", "DATA 3", "DATA 4"]
        writer = csv.DictWriter(f, fieldnames=header)
        writer.writeheader()

        data = 0
        while data < len(data_buffer):
            writer.writerow({
                "DATA 1": data_buffer[data],
                "DATA 2": data_buffer[data+1],
                "DATA 3": data_buffer[data+2],
                "DATA 4": data_buffer[data+3]
            })
            data1 += data_buffer[data]
            data2 += data_buffer[data+1]
            data3 += data_buffer[data+2]
            data4 += data_buffer[data+3]
            data += 4
    f.close()

    # isfileempty = os.stat(finalfile).st_size == 0
    with open(finalfile, "a", newline='') as final:
        header2 = ["Frequency", "V0", "I0", "R", "Theta", "X", "Y"]
        # header2 = ["Frequency", "R", "Theta", "X", "Y"]
        writer = csv.DictWriter(final, fieldnames=header2)
        if final.tell() == 0:
            writer.writeheader()
        writer.writerow(
            {
                "Frequency": HZ,
                "V0": keithley.voltage,
                "I0": hp.current_ac,
                "R": data1/points,
                "Theta": data2/points,
                "X": data3/points,
                "Y": data4/points
            }
        )
    final.close()
    print(nf.system_error())

    if HZ < 1E2:
        HZ += 1E1
    elif HZ >= 1E2 and HZ < 1E3:
        HZ += 1E2
    elif HZ >= 1E3 and HZ < 1E4:
        HZ += 1E3
    elif HZ >= 1E4 and HZ < 1E5:
        HZ += 1E4
    else:
        HZ += 1E5

print("Testing Done!")

dataframe = pd.read_csv('Data/Final.csv')
ln2w = np.log (4 * np.pi * (dataframe.Frequency)) 
plt.plot(ln2w, dataframe.X, 'r', label = "In Phase")
plt.plot(ln2w, dataframe.Y, 'g', label = 'Out of Phase') 
plt.xlabel('Ln(2\u03C9)')
plt.ylabel('Temperature Oscillation')
plt.grid(True)
plt.legend()
plt.show()
