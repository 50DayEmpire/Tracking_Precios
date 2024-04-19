from PyQt6 import QtWidgets, QtGui, uic
import sys

class MainWindow(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()

        # Carga el archivo .ui
        uic.loadUi(R'interfaz/gui/Tracking_main.ui', self)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    mainWin = MainWindow()
    mainWin.show()

    sys.exit(app.exec())
