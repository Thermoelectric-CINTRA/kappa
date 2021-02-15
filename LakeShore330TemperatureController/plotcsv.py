import sys
import random
import matplotlib
matplotlib.use('Qt5Agg')

from PyQt5 import QtCore, QtWidgets

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas, NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure

from pymeasure.instruments.lakeshore import LakeShore331
import matplotlib.pyplot as plt

class MplCanvas(FigureCanvas):

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.canvas = MplCanvas(self, width=5, height=4, dpi=100)
        self.setCentralWidget(self.canvas)
        self.temperatureController = LakeShore331("GPIB0::5")

        n_data = 7200
        self.xdata = list(range(n_data))
        self.ydata = [random.randint(0, 0) for i in range(n_data)]
        # self.ydata = [self.temperatureController.temperature_A]
        print(self.xdata, self.ydata)
        self.update_plot()

        # self.show()

        # Setup a timer to trigger the redraw by calling update_plot.
        self.timer = QtCore.QTimer()
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.update_plot)
        self.timer.start()

        toolbar = NavigationToolbar(self.canvas, self)

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(toolbar)
        layout.addWidget(self.canvas)

        widget = QtWidgets.QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

        self.show()

    def update_plot(self):
        # Drop off the first y element, append a new one.
        # self.ydata = self.ydata[1:] + [random.randint(0, 10)]
        # self.xdata = self.xdata[1:] + [self.xdata[len(self.xdata)-1] + 1]
        self.ydata = self.ydata[1:] + [self.temperatureController.temperature_A]
        # self.ydata = [self.temperatureController.temperature_A]
        print(self.xdata, self.ydata)
        self.canvas.axes.cla()  # Clear the canvas.
        self.canvas.axes.plot(self.xdata, self.ydata, '-b')
        # Trigger the canvas to update and redraw.
        self.canvas.draw()

        # plt.plot(self.xdata, self.ydata, 'r')
        # plt.show()
        


app = QtWidgets.QApplication(sys.argv)
w = MainWindow()
app.exec_()