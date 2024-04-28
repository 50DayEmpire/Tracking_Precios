from PyQt6.QtWidgets import QApplication, QMainWindow, QDialog, QMessageBox, QHeaderView
from PyQt6.QtCore import QTimer, QPropertyAnimation, Qt, pyqtSignal
from PyQt6 import uic
import sys
import os
from PyQt6.QtGui import QFont, QPixmap
import funciones as f
import json

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
        uic.loadUi("Interfaz/gui/Tracking_main.ui", self)
        self.resize(800, 600)  # Tamaño de la ventana 

        # Conectar señales a ranura
        self.btnGallo.clicked.connect(self.Gallo)
        self.btnSycom.clicked.connect(self.Colonia)
        self.btnJets.clicked.connect(self.Jestereo)
        self.btnTecknos.clicked.connect(self.Motomundo)
        self.btnLadyLee.clicked.connect(self.Lee)
        self.btnRadioshack.clicked.connect(self.Jordan)


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
        #DiseñoTabla        
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.tableWidget.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.Interactive)
        #Scollbar
            
        self.nombreTienda = t[0]
        pixmap = QPixmap(t[0])
        self.empresa.setPixmap(pixmap)
        self.ventanaUrl = Anadir_URL(self,t[1]) #Pasa la tabla a Anadir_URL
        
        self.btnatras.clicked.connect(self.back_to_main_window)
        self.btnactualizar.clicked.connect(self.act)
        self.btnPlusUrl.clicked.connect(self.crear_URL)

    def act(self):
        f.actualizar(self)

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
        uic.loadUi("Interfaz/gui/URL.ui", self)        
        self.resize(800, 600)  # Tamaño de la ventana
                        
        #volver
        self.btnatras.clicked.connect(self.back_to_main_window)
        #buscar producto
        self.lupa.clicked.connect(self.buscar)
        #Agregar un producto a la lista de tracking
        self.btnProducto.clicked.connect(self.Anadir_producto)
        
    def back_to_main_window(self):
        self.ventanaAnterior.show()
        self.textEdit.clear()
        self.nproduct.clear()
        f.vaciar()
        self.close()

    def buscar(self):
        url = self.textEdit.toPlainText()
        if url:
             # Ejecutar la búsqueda si se ingreso una url
            os.system("cd "+ os.path.dirname(os.path.abspath(__file__)) + "/../tracking && scrapy crawl " + self.tracker + " -O temp.json -a url="+url)
            self.btnProducto.setStyleSheet("background-color: rgb(87, 114, 209); color: white;") 
            self.btnProducto.setCursor(Qt.CursorShape.PointingHandCursor)

            with open('tracking/temp.json') as file:
                data = json.load(file)
            nombre_producto = data[0]["nombre"] if data else ""
            estilo = "font-size: 20px; color: white; text-align: center;"
            self.nproduct.setStyleSheet(estilo)
            self.nproduct.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.nproduct.setText(nombre_producto)
            
            self.mostrar_ultima_imagen()

        else:
             # Mostrar un mensaje de advertencia si no hay texto ingresado
            QMessageBox.warning(self, "Advertencia", "Por favor, ingrese una URL antes de hacer clic en el botón de búsqueda.")

    def mostrar_ultima_imagen(self):
        # Obtener la ruta de la última imagen agregada a una carpeta
        ruta_carpeta_imagenes = "tracking/imagenes/" + f.archivoActual()
        print(ruta_carpeta_imagenes)
        pixmap = QPixmap(ruta_carpeta_imagenes)
        pixmap_ajustada = pixmap.scaledToWidth(self.imgp.width())  # Ajustar al ancho del QLabel
        self.imgp.setPixmap(pixmap_ajustada)

    def Anadir_producto(self):
        f.guardarTracker()
        

def ejecutar():
    app = QApplication(sys.argv)

    #Creacion de ventanas
    global mainWin
    splash = Splash()
    mainWin = MainWindow()
    thirdWin1 = tienda(["interfaz/gui/imagenes/imgp/GMG.png","tracking_spider_GMG"])
    thirdWin2 = tienda(["interfaz/gui/imagenes/imgp/sycom.png","tracking_sycom"])
    thirdWin3 = tienda(["interfaz/gui/imagenes/imgp/Jetstereo.png","tracking_spider_jetstereo"])
    thirdWin4 = tienda(["interfaz/gui/imagenes/imgp/Tecknos.png","N/A"])
    thirdWin5 = tienda(["interfaz/gui/imagenes/imgp/LadyLee.png","N/A"])
    thirdWin6 = tienda(["interfaz/gui/imagenes/imgp/Radioshack.png","N/A"])

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