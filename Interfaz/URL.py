from PyQt6 import uic
from PyQt6.QtWidgets import QApplication
class URL():
    def __init__(self):
        self.login = uic.loadUi("Interfaz/gui/URL.ui")
        self.login.show()


class WURL():
    def __init__(self):
        self.app = QApplication([])
        self.login = URL() 
        self.app.exec()