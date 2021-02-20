from pymeasure.instruments.lakeshore import LakeShore330

temperature = LakeShore330("GPIB0::5")
gain = temperature.gain
print(gain)
temperature.gain = 50
print(temperature.gain)

reset = temperature.reset
print(reset)
rate = temperature.rate
print(rate)

temperature.reset = 20
print(temperature.reset)