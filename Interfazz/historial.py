from PyQt6 import uic
from PyQt6.QtWidgets import QApplication
# from PyQt6.QtWidgets import QMessageBox

class Historial():
    def __init__(self):
        self.login = uic.loadUi("gui/historial.ui")
        self.login.show()

class Whistorial():
    def __init__(self):
        self.app = QApplication([])
        self.login = Historial() 
        self.app.exec()
