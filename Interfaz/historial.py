from PyQt6 import uic
from PyQt6.QtWidgets import QApplication
#import funciones as f
# from PyQt6.QtWidgets import QMessageBox

class Historial():
    def __init__(self):
        self.login = uic.loadUi("Interfaz/gui/historial.ui")
        self.login.show()


class URL():
    def __init__(self):
        self.ventana = uic.loadUi("Interfaz/gui/URL.ui")
        self.ventana.show()


class Whistorial():
    def __init__(self):
        self.app = QApplication([])
        self.login = Historial() 
        
        self.app.exec()

app = Whistorial()
