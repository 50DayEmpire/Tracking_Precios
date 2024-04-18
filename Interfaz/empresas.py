from PyQt6 import QtWidgets, uic
import sys

class MainWindow(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()

        # Carga el archivo .ui
        uic.loadUi(R'gui/Tracking_main.ui', self)

        # Cambia la imagen de fondo del label_2A
        self.btnGallo.setStyleSheet("gui/imagenes/GMG.png")
        self.btnColonia.setStyleSheet("gui/imagenes/Colonia.png")
        self.btnJets.setStyleSheet("gui/imagenes/Jestereo.png")
        self.btnMoto.setStyleSheet("gui/imagenes/Motomundo.png")
        self.btnLadyLee.setStyleSheet("gui/imagenes/LadyLee.png")
        self.btnJordan.setStyleSheet("gui/imagenes/Jordan.png")
        

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    mainWin = MainWindow()
    mainWin.show()

    sys.exit(app.exec())