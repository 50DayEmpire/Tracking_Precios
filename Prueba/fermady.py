from PyQt5.QtWidgets import QApplication

from login import Login

class Fermady():
    def __init__(self):
        self.app = QApplication([])
        self.login = Login() 

        self.app.exec()