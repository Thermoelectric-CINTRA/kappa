from PyQt5.QtWidgets import QApplication, QMainWindow
import sys

class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.setWindowTitle("3 \u03C9 Measurements")

        self.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main = MainWindow()
    sys.exit(app.exec_())