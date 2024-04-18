
from PyQt6 import QtWidgets, uic
import sys

class MainWindow(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()

        # Carga el archivo .ui
        uic.loadUi(R'C:\Users\Richard López\Documents\GitHub\Tracking_Precios\Interfaz\gui\Tracking_main.ui', self)

        # Cambia la imagen de fondo del label_2A
        self.btnGallo.setStyleSheet("image: url('C:/Users/Richard López/Documents/GitHub/Tracking_Precios/Interfaz/gui/imagenes/GMG.png');")
        self.btnColonia.setStyleSheet("image: url('C:/Users/Richard López/Documents/GitHub/Tracking_Precios/Interfaz/gui/imagenes/Colonia.png');")
        self.btnJets.setStyleSheet("image: url('C:/Users/Richard López/Documents/GitHub/Tracking_Precios/Interfaz/gui/imagenes/Jetstereo.png');")
        self.btnMoto.setStyleSheet("image: url('C:/Users/Richard López/Documents/GitHub/Tracking_Precios/Interfaz/gui/imagenes/Motomundo.png');")
        self.btnLadyLee.setStyleSheet("image: url('C:/Users/Richard López/Documents/GitHub/Tracking_Precios/Interfaz/gui/imagenes/LadyLee.jpg');")
        self.btnJordan.setStyleSheet("image: url('C:/Users/Richard López/Documents/GitHub/Tracking_Precios/Interfaz/gui/imagenes/Jordan.png');")
        

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    mainWin = MainWindow()
    mainWin.show()

    sys.exit(app.exec())
