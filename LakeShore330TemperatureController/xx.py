import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import datetime

def LivePlot(self):
    def animate(self):
        date = datetime.date.today()
        fileName = "temperature_{}.csv".format(date)
        data = pd.read_csv('D:/CINTRA/kappa/LakeShore330TemperatureController/Data/{}'.format(fileName))
        x_values = data['Timestamp']
        y_values = data['Temperatures']
        plt.cla()
        plt.plot(x_values, y_values)
        plt.xlabel('Time')
        plt.ylabel('Temperatures')
        plt.title('LakeShore330')
        plt.gcf().autofmt_xdate()
        plt.tight_layout()

    ani = FuncAnimation(plt.gcf(), animate, 1000)

    plt.tight_layout()
    plt.show()