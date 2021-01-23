import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

frequency = np.arange(1, 1000, 1)
TTC = 1e-3

V0 = 0.7
TCR = 2.5e-3
wdith = 0.252e-3
length = 1.73e-3
thickness = 100e-9
Resistance = 20
Kappa = 10.2

V3w = (V0**3 * TCR * wdith) / ((16 * Resistance * Kappa * thickness * length) * (1 + frequency**2 * TTC**2))

plt.plot(frequency**2, 1/V3w)
plt.xlabel('Frequency $\u03C9^2$')
plt.ylabel('Re($V_{3\u03C9}$)$^{-1}$')
plt.title('Inverse real part of the 3\u03C9 voltage as function of $\u03C9^2$', pad=20)
plt.show()