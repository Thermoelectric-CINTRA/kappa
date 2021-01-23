import sys
import matplotlib
matplotlib.use('Qt5Agg')

from PyQt5 import QtCore, QtGui, QtWidgets

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure

import numpy as np


class MplCanvas(FigureCanvasQTAgg):

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.widgets()

        self.show()
    
    def widgets(self):
        self.sc = MplCanvas(self, width=5, height=4, dpi=100)
        # Create toolbar, passing canvas as first parament, parent (self, the MainWindow) as second.
        toolbar = NavigationToolbar(self.sc, self)

        grid_layout = QtWidgets.QGridLayout()

        low_freq_label = QtWidgets.QLabel()
        high_freq_label = QtWidgets.QLabel()
        ttc_label = QtWidgets.QLabel()
        tcr_label = QtWidgets.QLabel()
        v0_label = QtWidgets.QLabel()
        width_label = QtWidgets.QLabel()
        length_label = QtWidgets.QLabel()
        thickness_label = QtWidgets.QLabel()
        resistance_label = QtWidgets.QLabel()
        kappa_label = QtWidgets.QLabel()

        low_freq_label.setText('Low Freq:')
        high_freq_label.setText('High Freq:')
        ttc_label.setText('TTC:')
        tcr_label.setText('TCR:')
        v0_label.setText('Voltage:')
        width_label.setText('Width:')
        length_label.setText('Length:')
        thickness_label.setText('Thinckness:')
        resistance_label.setText('Resistance:')
        kappa_label.setText('Kappa:')

        self.low_freq = QtWidgets.QLineEdit()
        self.high_freq = QtWidgets.QLineEdit()
        self.ttc = QtWidgets.QLineEdit()
        self.tcr = QtWidgets.QLineEdit()
        self.v0 = QtWidgets.QLineEdit()
        self.width = QtWidgets.QLineEdit()
        self.length = QtWidgets.QLineEdit()
        self.thickness = QtWidgets.QLineEdit()
        self.resistance = QtWidgets.QLineEdit()
        self.kappa = QtWidgets.QLineEdit()

        calculate = QtWidgets.QPushButton()
        calculate.setText('Calculate')
        calculate.clicked.connect(self.updateFigure)

        grid_layout.addWidget(low_freq_label, 0, 0)
        grid_layout.addWidget(high_freq_label, 1, 0)
        grid_layout.addWidget(ttc_label, 0, 2)
        grid_layout.addWidget(tcr_label, 1, 2)
        grid_layout.addWidget(v0_label, 2, 0)
        grid_layout.addWidget(resistance_label, 2, 2)
        grid_layout.addWidget(width_label, 3, 0)
        grid_layout.addWidget(length_label, 4, 0)
        grid_layout.addWidget(thickness_label, 3, 2)
        grid_layout.addWidget(kappa_label, 4, 2)

        grid_layout.addWidget(self.low_freq, 0, 1)
        grid_layout.addWidget(self.high_freq, 1, 1)
        grid_layout.addWidget(self.ttc, 0, 3)
        grid_layout.addWidget(self.tcr, 1, 3)
        grid_layout.addWidget(self.v0, 2, 1)
        grid_layout.addWidget(self.resistance, 2, 3)
        grid_layout.addWidget(self.width, 3, 1)
        grid_layout.addWidget(self.length, 4, 1)
        grid_layout.addWidget(self.thickness, 3, 3)
        grid_layout.addWidget(self.kappa, 4, 3)

        grid_layout.addWidget(calculate, 5, 3)

        # Parameters
        self.low_freq.setText('100')
        self.high_freq.setText('1e3')
        self.ttc.setText('1e-3')
        self.v0.setText('0.7')
        self.tcr.setText('2.5e-3')
        self.width.setText('0.252e-3')
        self.length.setText('1.73e-3')
        self.thickness.setText('100e-9')
        self.resistance.setText('20')
        self.kappa.setText('10.2')

        self.FREQUENCY = np.arange(float(self.low_freq.text()), float(self.high_freq.text()), 1)
        self.TTC = float(self.ttc.text())
        self.V0 = float(self.v0.text())
        self.TCR = float(self.tcr.text())
        self.WIDTH = float(self.width.text())
        self.LENGTH = float(self.length.text())
        self.THICKNESS = float(self.thickness.text())
        self.RESISTANCE = float(self.resistance.text())
        self.KAPPA = float(self.kappa.text())
        # Real part of the 3 omega voltage as function of omega square
        self.V3w = (self.V0**3 * self.TCR * self.WIDTH) / ((16 * self.RESISTANCE * self.KAPPA * self.THICKNESS * self.LENGTH) * (1 + self.FREQUENCY**2 * self.TTC**2))

        self.sc.axes.plot(self.FREQUENCY**2, 1/self.V3w)

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(toolbar)
        layout.addLayout(grid_layout)
        layout.addWidget(self.sc)

        # Create a placeholder widget to hold our toolbar and canvas.
        widget = QtWidgets.QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

    def updateFigure(self):
        self.FREQUENCY = np.arange(float(self.low_freq.text()), float(self.high_freq.text()), 1)
        self.TTC = float(self.ttc.text())
        self.V0 = float(self.v0.text())
        self.TCR = float(self.tcr.text())
        self.WIDTH = float(self.width.text())
        self.LENGTH = float(self.length.text())
        self.THICKNESS = float(self.thickness.text())
        self.RESISTANCE = float(self.resistance.text())
        self.KAPPA = float(self.kappa.text())
        self.V3w = (self.V0**3 * self.TCR * self.WIDTH) / ((16 * self.RESISTANCE * self.KAPPA * self.THICKNESS * self.LENGTH) * (1 + self.FREQUENCY**2 * self.TTC**2))

        self.sc.axes.plot(self.FREQUENCY**2, 1/self.V3w)
        self.sc.draw()

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    main = MainWindow()
    sys.exit(app.exec_())