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
    def __init__(self,t):
        super().__init__()
        uic.loadUi(("Interfaz/gui/Tracking_GMG.ui"), self)
        self.resize(800, 600)  # Tamaño de la ventana 
        self.empresa.setText(t[0])
        font = QFont("Arial", 20)
        font.setBold(True)  
        self.empresa.setFont(font)  
        self.ventanaUrl = Anadir_URL(self,t[1])
        
        self.btnatras.clicked.connect(self.back_to_main_window)
        self.btnPlusUrl.clicked.connect(self.crear_URL)

    def crear_URL(self):
        self.ventanaUrl.show()
        self.hide()
        
    def back_to_main_window(self):
        self.close() 
        mainWin.show()

class Anadir_URL(QMainWindow):
    def __init__(self,ventanaAnterior,tracker):
        super().__init__()
        self.ventanaAnterior = ventanaAnterior
        self.tracker = tracker
        uic.loadUi("interfaz/gui/URL.ui", self)
        self.resize(800, 600)  # Tamaño de la ventana
        #volver
        self.btnatras.clicked.connect(self.back_to_main_window)
        #evaluar un producto con un url
        self.btnProducto.clicked.connect(self.Anadir_producto)
        
    def back_to_main_window(self):
            self.ventanaAnterior.show()
            self.close()

    def Anadir_producto(self):
        url = self.textEdit.toPlainText()
        print(self.tracker)
        #print("cd "+ os.path.dirname(os.path.abspath(__file__)) + "/../tracking && scrapy crawl " + self.tracker + " -o precio.jsonl -a url="+url)
        #Falta ejecutar el tracker Adecuado
        os.system("cd "+ os.path.dirname(os.path.abspath(__file__)) + "/../tracking && scrapy crawl " + self.tracker + " -o precio.jsonl -a url="+url)
        #despues de agregar la URL

def ejecutar():
    app = QApplication(sys.argv)

    #Creacion de ventanas
    global mainWin
    splash = Splash()
    mainWin = MainWindow()
    thirdWin1 = tienda(["GALLO MÁS GALLO","tracking_spider_GMG"])
    thirdWin2 = tienda(["LA COLONIA","N/A"])
    thirdWin3 = tienda(["JETSTEREO","tracking_spider_jetstereo"])
    thirdWin4 = tienda(["MOTOMUNDO","N/A"])
    thirdWin5 = tienda(["LADY LEE","N/A"])
    thirdWin6 = tienda(["EL JORDAN","N/A"])

    # Conectar señales y ranuras para controlar el flujo de la aplicación
    splash.splashClosed.connect(mainWin.show)
    mainWin.GalloClicked.connect(thirdWin1.show)
    mainWin.ColoniaClicked.connect(thirdWin2.show)
    mainWin.JestereoClicked.connect(thirdWin3.show)
    mainWin.MotomundoClicked.connect(thirdWin4.show)
    mainWin.LeeClicked.connect(thirdWin5.show)
    mainWin.JordanClicked.connect(thirdWin6.show)

    splash.show()

    sys.exit(app.exec())