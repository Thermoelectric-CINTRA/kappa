import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import datetime

def LivePlot(self):
    def animate(self):
        # date = datetime.date.today()
        # fileName = "temperature_{}.csv".format(date)
        fileName = "resistance_10K_to_475K.csv"
        data = pd.read_csv('D:/CINTRA/kappa/LakeShore330TemperatureController/Data/{}'.format(fileName))
        x_values = data['Temperatures'][0:9]
        y_values = data['Resistance'][0:9]
        plt.cla()
        plt.plot(x_values, y_values)
        plt.xlabel('Temperature')
        plt.ylabel('Resistance')
        plt.title('LakeShore330')
        plt.gcf().autofmt_xdate()
        plt.tight_layout()

    ani = FuncAnimation(plt.gcf(), animate, 100)

    plt.tight_layout()
    plt.show()