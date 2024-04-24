from PyQt6.QtWidgets import QApplication, QMainWindow, QDialog
from PyQt6.QtCore import QTimer, QPropertyAnimation, Qt, pyqtSignal
from PyQt6 import uic
import sys
import os
from PyQt6.QtGui import QFont, QPixmap


class Splash(QMainWindow):
    splashClosed = pyqtSignal() 

    def __init__(self):
        super().__init__()

        self.setWindowFlag(Qt.WindowType.FramelessWindowHint)  # Elimina el marco de la ventana
        uic.loadUi("interfaz/gui/inicio.ui", self)

        self.show_timer = QTimer(self)
        self.show_timer.timeout.connect(self.close_splash)
        self.show_timer.start(3000)

    def close_splash(self):
        self.show_timer.stop()
        self.fade_animation = QPropertyAnimation(self, b"windowOpacity")
        self.fade_animation.setDuration(1000)
        self.fade_animation.setStartValue(1.0)
        self.fade_animation.setEndValue(0.0)
        self.fade_animation.finished.connect(self.emit_splash_closed)
        self.fade_animation.start()

    def emit_splash_closed(self):
        self.close()
        self.splashClosed.emit()  


class MainWindow(QDialog):
    GalloClicked = pyqtSignal()  
    ColoniaClicked = pyqtSignal() 
    JestereoClicked = pyqtSignal() 
    MotomundoClicked = pyqtSignal() 
    LeeClicked = pyqtSignal() 
    JordanClicked = pyqtSignal() 

    

    def __init__(self):
        super().__init__()
        uic.loadUi("interfaz/gui/Tracking_main.ui", self)
        self.resize(800, 600)  # Tamaño de la ventana 

        # Conectar señales a ranura
        self.btnGallo.clicked.connect(self.Gallo)
        self.btnColonia.clicked.connect(self.Colonia)
        self.btnJets.clicked.connect(self.Jestereo)
        self.btnMoto.clicked.connect(self.Motomundo)
        self.btnLadyLee.clicked.connect(self.Lee)
        self.btnJordan.clicked.connect(self.Jordan)


    def Gallo(self):
        self.GalloClicked.emit()  
        self.close()

    def Colonia(self):
        self.ColoniaClicked.emit()  
        self.close()

    def Jestereo(self):
        self.JestereoClicked.emit()  
        self.close()

    def Motomundo(self):
        self.MotomundoClicked.emit()  
        self.close()

    def Lee(self):
        self.LeeClicked.emit()  
        self.close()

    def Jordan(self):
        self.JordanClicked.emit()  
        self.close()

class tienda(QDialog):
    URLClicked = pyqtSignal()

    def __init__(self,t):
        super().__init__()
        uic.loadUi(("Interfaz/gui/Tracking_GMG.ui"), self)
        self.resize(800, 600)  # Tamaño de la ventana 
        self.empresa.setText(t)
        font = QFont("Arial", 20)
        font.setBold(True)  
        self.empresa.setFont(font)  
        
        self.btnatras.clicked.connect(self.back_to_main_window)
        self.btnPlusUrl.clicked.connect(self.URL)

    def URL(self):
        self.URLClicked.emit()  
        self.close() 
        
    def back_to_main_window(self):
        self.close() 
        mainWin.show()

#clase añadir URL    
class Anadir_URL(QMainWindow):
    backClicked = pyqtSignal()

    def __init__(self):
        super().__init__()
        uic.loadUi("interfaz/gui/URL.ui", self)
        self.resize(800, 600)  # Tamaño de la ventana
        #volver
        self.btnatras.clicked.connect(self.back_to_main_window)
        #evaluar un producto con un url
        self.btnProducto.clicked.connect(self.Anadir_producto)
        
    def back_to_main_window(self):
            self.backClicked.emit()
            self.close()

    def Anadir_producto(self):
        #Falta ejecutar el tracker Adecuado
        os.system("cd "+ os.path.dirname(os.path.abspath(__file__)) + "/../tracking" +" && scrapy crawl tracking_spider_jetstereo -o precio.jsonl -a url="+url)
        #despues de agregar la URL
        print("Agregar url y mostrar imagen")



if __name__ == "__main__":
    app = QApplication(sys.argv)

    splash = Splash()
    mainWin = MainWindow()
    thirdWin1 = tienda("GALLO MÁS GALLO")
    thirdWin2 = tienda("LA COLONIA")
    thirdWin3 = tienda("JETSTEREO")
    thirdWin4 = tienda("MOTOMUNDO")
    thirdWin5 = tienda("LADY LEE")
    thirdWin6 = tienda("EL JORDAN")


    fourthWin6 = Anadir_URL()
    fourthWin5 = Anadir_URL()
    fourthWin4 = Anadir_URL()
    fourthWin3 = Anadir_URL()
    fourthWin2 = Anadir_URL()
    fourthWin1 = Anadir_URL()

    # Conectar señales y ranuras para controlar el flujo de la aplicación
    splash.splashClosed.connect(mainWin.show)
    mainWin.GalloClicked.connect(thirdWin1.show)
    mainWin.ColoniaClicked.connect(thirdWin2.show)
    mainWin.JestereoClicked.connect(thirdWin3.show)
    mainWin.MotomundoClicked.connect(thirdWin4.show)
    mainWin.LeeClicked.connect(thirdWin5.show)
    mainWin.JordanClicked.connect(thirdWin6.show)

    thirdWin1.URLClicked.connect(fourthWin1.show)
    thirdWin2.URLClicked.connect(fourthWin2.show)
    thirdWin3.URLClicked.connect(fourthWin3.show)
    thirdWin4.URLClicked.connect(fourthWin4.show)
    thirdWin5.URLClicked.connect(fourthWin5.show)
    thirdWin6.URLClicked.connect(fourthWin6.show)

    splash.show()

    sys.exit(app.exec())

def ejecutar():
    app = QApplication(sys.argv)

    global splash, mainWin, thirdWin1
    splash = Splash()
    mainWin = MainWindow()
    thirdWin1 = tienda("GALLO MÁS GALLO")
    thirdWin2 = tienda("LA COLONIA")
    thirdWin3 = tienda("JETSTEREO")
    thirdWin4 = tienda("MOTOMUNDO")
    thirdWin5 = tienda("LADY LEE")
    thirdWin6 = tienda("EL JORDAN")


    fourthWin6 = Anadir_URL()
    fourthWin5 = Anadir_URL()
    fourthWin4 = Anadir_URL()
    fourthWin3 = Anadir_URL()
    fourthWin2 = Anadir_URL()
    fourthWin1 = Anadir_URL()

    # Conectar señales y ranuras para controlar el flujo de la aplicación
    splash.splashClosed.connect(mainWin.show)
    mainWin.GalloClicked.connect(thirdWin1.show)
    mainWin.ColoniaClicked.connect(thirdWin2.show)
    mainWin.JestereoClicked.connect(thirdWin3.show)
    mainWin.MotomundoClicked.connect(thirdWin4.show)
    mainWin.LeeClicked.connect(thirdWin5.show)
    mainWin.JordanClicked.connect(thirdWin6.show)

    thirdWin1.URLClicked.connect(fourthWin1.show)
    thirdWin2.URLClicked.connect(fourthWin2.show)
    thirdWin3.URLClicked.connect(fourthWin3.show)
    thirdWin4.URLClicked.connect(fourthWin4.show)
    thirdWin5.URLClicked.connect(fourthWin5.show)
    thirdWin6.URLClicked.connect(fourthWin6.show)

    fourthWin1.backClicked.connect(thirdWin1.show)
    fourthWin2.backClicked.connect(thirdWin2.show)
    fourthWin3.backClicked.connect(thirdWin3.show)
    fourthWin4.backClicked.connect(thirdWin4.show)
    fourthWin5.backClicked.connect(thirdWin5.show)
    fourthWin6.backClicked.connect(thirdWin6.show)

    splash.show()

    sys.exit(app.exec())