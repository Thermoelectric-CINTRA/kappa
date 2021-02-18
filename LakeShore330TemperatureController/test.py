from pymeasure.instruments.lakeshore import LakeShore331

controller = LakeShore331("GPIB0::5")

controller.setpoint_1 = 300          # Change the setpoint to 50 K
print(controller.setpoint_1)        # Print the current setpoint for loop 1

controller.heater_range = 'low'     # Change the heater range to Low
controller.wait_for_temperature()   # Wait for the temperature to stabilize
print(controller.temperature_A)     # Print the temperature at sensor A