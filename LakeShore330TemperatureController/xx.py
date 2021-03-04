# from datetime import datetime as dt
# from pymeasure.instruments.hp import HP34401A
# from pymeasure.instruments.keysight import Keysight33210A
# from pymeasure.instruments.nf import LI5660
# import time
# import csv


# # now = datetime.now().time() # time object

# # print("now =", now)
# # print("type(now) =", type(now))

# # hp = HP34401A("GPIB0::2")
# # print("Current", hp.current_ac)

# # keysigh = Keysight33210A("GPIB0::4")
# # print("Vin", keysigh.amplitude)

# nf = LI5660("GPIB0::1")
# # Function Generator
# # keysight = Keysight33210A("GPIB0::4")
# # Current Meter
# # hp = HP34401A("GPIB0::2")
# # points = 1
# # temp = dt.now().time()
# # 
# # nf.data1_format("Mlinear")      # R
# # nf.data2_format("Phase")        # Theta
# # nf.data3_format("Real")         # X
# # nf.data4_format("Imaginary")    # Y

# # # nf.reference_signal(source="Internal")
# # nf.coupling("AC")
# # nf.grounding("Ground") # Float or Ground
# # nf.input_terminal("AB")
# # nf.primary_harmonic("Off")

# # # nf.primary_phase_shift(theta)
# # nf.oscillator_amplitude(1)
# # nf.timer_state("On")
# # nf.interval(0.1)
# nf.clear_all_buffer()
# # # phaseshift = nf.fetch       # Get the phase shift after setting the new internal oscillationg frequency
# # nf.data_feed("Buffer1",30)
# # nf.data_feed_control("Buffer1", "Always")
# # nf.data_points("Buffer1",points)
# # nf.source_trigger("Bus")
# # # theta -= phaseshift[1]
# # # nf.primary_phase_shift(0)     # Counter the phase shift
# # nf.delay(0)
# # nf.initiate()
# # print("Operation condition: ", nf.status_operation_condition)

# # nf.trigger()

# # while nf.status_operation_condition < 256:
# #     # print(nf.status_operation_condition)
# #     print(nf.buffer1_count, "/{}".format(points))

# # data_buffer = nf.get_buffer("Buffer1", points, 0)
# # current = hp.current_ac
# # vin = keysight.amplitude
# # time.sleep(1)
# # fileName = "resistance_lockin.csv"
# # with open(fileName, 'a', newline='') as csvfile:
# #     header = ["Timestamp", "Temperature", "R", "Theta", "X", "Y", "Current", "Vin"]
# #     writer = csv.DictWriter(csvfile, fieldnames=header)
# #     if csvfile.tell() == 0:
# #         writer.writeheader()
# #     writer.writerow(
# #         {
# #             "Timestamp": time,
# #             "Temperature": temp,
# #             "R": data_buffer[0],
# #             "Theta": data_buffer[1],
# #             "X": data_buffer[2],
# #             "Y": data_buffer[3],
# #             "Current": current,
# #             "Vin": vin
# #         }
# #     )
# # csvfile.close()

import pyfirmata
import time

board = pyfirmata.Arduino('COM3')
it = pyfirmata.util.Iterator(board)
it.start()
analog_input = board.get_pin('a:0:i')
while True:
    analog_value = analog_input.read()
    print(analog_value)
    time.sleep(1)