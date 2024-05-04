from PyQt6.QtWidgets import QApplication, QMainWindow, QDialog, QMessageBox, QHeaderView, QTableWidgetItem, QAbstractItemView
from PyQt6.QtCore import QTimer, QPropertyAnimation, Qt, pyqtSignal, QUrl, QRegularExpression
from PyQt6 import uic, QtCore
import sys
from PyQt6.QtGui import QPixmap, QFont, QDesktopServices, QRegularExpressionValidator
from os import path
import pygame
import funciones as f
import json
from os.path import abspath, dirname, join, getsize
import subprocess
import re 

class miTableWidgetItem(QTableWidgetItem):
    def __init__(self,objeto):
        super().__init__()
        self.objetoOculto = objeto

class Splash(QMainWindow):
    splashClosed = pyqtSignal()
    actualizacionGeneralEncendida=False

    def __init__(self):
        super().__init__()

        self.setWindowFlag(Qt.WindowType.FramelessWindowHint)  # Elimina el marco de la ventana
        uic.loadUi("interfaz/gui/inicio.ui", self)
        
        self.close_splash()
        # self.show_timer = QTimer(self)
        # self.show_timer.timeout.connect(self.close_splash)
        # self.show_timer.start(3000)

    def close_splash(self):
        #self.show_timer.stop()
        self.fade_animation = QPropertyAnimation(self, b"windowOpacity")
        self.fade_animation.setDuration(1000)
        self.fade_animation.setStartValue(1.0)
        self.fade_animation.setEndValue(0.0)
        self.fade_animation.finished.connect(self.emit_splash_closed)
        if Splash.actualizacionGeneralEncendida:
            self.updateGeneral()
        self.fade_animation.start()

    def emit_splash_closed(self):
        self.close()
        self.splashClosed.emit()

    def updateGeneral(self):
        f.actGeneral()        

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
        self.btnos.clicked.connect(self.nosotros)  
        self.ventana_nosotros = Nosotros

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

    def nosotros(self):
        self.ventana_nosotros = Nosotros()
        self.ventana_nosotros.show()
        self.hide()

class tienda(QDialog):
    def __init__(self,t,rutaImg):
        super().__init__()
        uic.loadUi(("Interfaz/gui/Tracking_GMG.ui"), self)
        self.resize(800, 600)  # Tamaño de la ventana 
        self.rutaImg = rutaImg
        self.nombreTienda = t[2]
        self.ingresarFila()
        #DiseñoTabla        
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.tableWidget.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        self.tableWidget.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Interactive)
        self.tableWidget.setColumnWidth(2, 0)
        self.tableWidget.setColumnHidden(2, True)#columna oculta
        
        #Scollbar
        pixmap = QPixmap(t[0])
        self.empresa.setPixmap(pixmap)
        self.ventanaUrl = Anadir_URL(self,t[1],rutaImg)
        
        self.btnatras.clicked.connect(self.back_to_main_window) #botones Tracking_GMG
        self.btnactualizar.clicked.connect(self.ingresarFila)
        self.btnPlusUrl.clicked.connect(self.crear_URL)
        
        #deshabilitar tablas:
        self.tableWidget.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)        
        self.tableWidget.cellDoubleClicked.connect(self.ventanaHistorial) #llamada        
        self.tableWidget.cellClicked.connect(self.obtenerFila) #para obtener
        #eliminar filas        
        self.btnEliminar_2.clicked.connect(self.eliminarFila)
        
    def act(self):
        f.actualizar(self)
    
    def vaciar(self):
        x=[]
        print("---------VACIAR TABLA ------------------")
        for row in range(self.tableWidget.rowCount()):
            for column in range(self.tableWidget.columnCount()): #---Aqui obtiene todos los nombres y los valores
                item = (self.tableWidget.item(row, column))
                if item is not None:
                    x.append(item.text())     
        for v in x:
            print(v)
        self.tableWidget.setRowCount(0)     

    def crear_URL(self):
        self.ventanaUrl.show()
        self.hide()

    def back_to_main_window(self):
        self.close() 
        mainWin.show()

    def ingresarFila(self):
        self.vaciar()
        productos = f.actualizar(self)
        if len(productos)==0:
            return

        for objeto in productos:
            self.tableWidget.insertRow(0)
            item = QTableWidgetItem(objeto.articulo)
            item2 = QTableWidgetItem(objeto.precio)
            item3 = miTableWidgetItem(objeto)
            self.tableWidget.setItem(0,0,item)
            self.tableWidget.setItem(0,1,item2)
            self.tableWidget.setItem(0,2,item3)

        for fila in range(self.tableWidget.rowCount()):
            item = self.tableWidget.item(fila, 1)
            if item is not None:
                item.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

    def ventanaHistorial(self, row, column):
        print(f"Doble click en la celda ({row},{column})")
        objeto = self.tableWidget.item(row,2)
        self.historial = Historial(self,objeto.objetoOculto)
        self.historial.show()
        self.hide()

    def obtenerFila(self, row, column):
        print(f"Estamos en la posición: ({row},{column})")              

    def eliminarFila(self, row):              
        lista = []  
        selected_rows = set(index.row() for index in self.tableWidget.selectedIndexes())
        for row in selected_rows:                  
            item = self.tableWidget.item(row, 0)
            if item is not None:
                lista.append(item.text())
            self.tableWidget.removeRow(row)
            print(f"La fila {row} fue eliminada. Datos: {lista}")         
        
        #f.borrar(self,lista)  #<===== buscar la forma de mandar una lista con los nombres de los articulos en las filas a borrar (para borrarlos del archivo .json tambien)
      
class Nosotros(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("Interfaz/gui/nosotros.ui", self)
       
        self.btnreg.clicked.connect(self.back_to_main_window)

    def back_to_main_window(self):
        self.close() 
        mainWin.show()

class Anadir_URL(QMainWindow):
    def __init__(self, ventanaAnterior, tracker, img):
        super().__init__()
        self.ventanaAnterior = ventanaAnterior
        self.tracker = tracker
        self.img = img  # Ruta de la segunda imagen
        pixmap = QPixmap(ventanaAnterior.rutaImg)
        uic.loadUi("interfaz/gui/URL.ui", self)
        self.resize(800, 600)  # Tamaño de la ventana
        self.btnlogo.setPixmap(pixmap)
        # Cargar y mostrar la segunda imagen
        pixmap_segunda = QPixmap(self.img)
        self.btnlogo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.btnlogo.setPixmap(pixmap_segunda)
    
        #volver
        self.btnatras.clicked.connect(self.back_or_confirm)
        #buscar producto
        self.lupa.clicked.connect(self.buscar)
        #Añadir producto en la lista de tracking
        self.btnProducto.clicked.connect(self.Anadir_producto)
        self.url = ""  # Inicializar la URL vacía
        

    #Funcion que verifica si la cadena ingresada tiene formato de una URL, utilizando el modulo re
    def es_url_valida(self, url):
        patron = re.compile(r'^https?://(?:www\.)?\w+\.\w+')
        return bool(patron.match(url))

    #solo preguntara esto si se realizo una busqueda
    def back_or_confirm(self):
        if self.url:
            reply = QMessageBox.question(self, "Confirmación", "¿Estás seguro de que quieres cancelar? Los cambios no se guardarán.",
                                        QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            if reply == QMessageBox.StandardButton.No:
                return
        self.back_to_main_window()

    def back_to_main_window(self):
        self.ventanaAnterior.show()
        self.textEdit.clear()
        self.nproduct.clear()
        self.imgp.clear()
        self.imgp.setText("Vista previa del producto")
        self.imgp.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.imgp.setStyleSheet("background-color: rgb(184, 184, 184);")
        f.vaciar()
        self.close()

    #Si el texEdit esta vacio dice que ingrese una url. si no infgresa url valida dice que no es valida 
    def buscar(self):
        url = self.textEdit.toPlainText()
        if not url:
            QMessageBox.warning(self, "Advertencia", "Por favor, ingrese una URL antes de hacer clic en el botón de búsqueda.")
            return False

        if self.es_url_valida(url):
            self.btnProducto.setEnabled(True)
            subprocess.run(["scrapy", "crawl", self.tracker, "-O", "temp.json", "-a", "url="+url], cwd=join(dirname(abspath(__file__)), "../tracking"))

            if getsize('tracking/temp.json') > 0:
                with open('tracking/temp.json','r', encoding='utf-8') as file:
                    data = json.load(file)
                nombre_producto = data[0]["nombre"] if data else ""

                font_size = min(self.nproduct.height() // 2, self.nproduct.width() // len(nombre_producto))  
                font_size = max(14, font_size)
                estilo = f"font-size: {font_size}px; color: white; text-align: center;"
                self.nproduct.setStyleSheet(estilo)
                self.nproduct.setAlignment(Qt.AlignmentFlag.AlignCenter)
                self.nproduct.setText(nombre_producto)

                self.mostrar_ultima_imagen()
                self.url = url  
        else:
            QMessageBox.warning(self, "Advertencia", "La URL ingresada no es válida. Por favor, ingrese una URL válida.")
            return False

    def mostrar_ultima_imagen(self):
        ruta_carpeta_imagenes = "tracking/imagenes/" + f.archivoActual()
        self.imgp.setStyleSheet("background-color: transparent;")
        if path.exists(ruta_carpeta_imagenes):
            pixmap = QPixmap(ruta_carpeta_imagenes)
            pixmap_ajustada = pixmap.scaled(self.imgp.size(), Qt.AspectRatioMode.KeepAspectRatio)
            self.imgp.setPixmap(pixmap_ajustada)
            self.imgp.setAlignment(Qt.AlignmentFlag.AlignCenter)

    def Anadir_producto(self):
        if self.url:
            self.ventanaAnterior.vaciar()
            f.guardarTracker()
            self.back_to_main_window()
            self.ventanaAnterior.ingresarFila()
        else:           
            QMessageBox.warning(self, "Advertencia", "Por favor, Haga la busqueda de su producto.")

class Historial(QMainWindow): 
    def __init__(self,ventanaAnterior,objeto):
        super().__init__()
        self.ventanaAnterior = ventanaAnterior
        self.objeto = objeto
        uic.loadUi("Interfaz/gui/historial.ui", self) 
        self.resize(800, 600)
        self.tablahist.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.btnatras.clicked.connect(self.back_to_main_window)
        self.prueba()  
        self.btncomprar.clicked.connect(self.sitio_web)
        self.btnalerta.clicked.connect(self.notificacion)
        pygame.init()
        self.lbnoti.setStyleSheet("background-color: green; color: white; font-weight: bold; padding: 10px;")
        self.lbnoti.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lbnoti.hide()
        validator = QRegularExpressionValidator(QRegularExpression("[0-9]+"))  # Permite solo números   
        self.textalerta.setValidator(validator)
        
    def back_to_main_window(self):
            self.ventanaAnterior.show()
            self.lbproducto.clear()
            self.lbproducto.setText("Imagen del producto")
            self.lbproducto.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.lbproducto.setStyleSheet("background-color: rgb(206, 206, 206);")
            self.close()
        
    def prueba(self):                                           
        print("nombre dl articulo//", self.objeto.articulo)
        self.nproducto.setText(self.objeto.articulo)
        self.nproducto.setAlignment(Qt.AlignmentFlag.AlignCenter)
        # Tabla
        self.tablahist.setRowCount(1)
        # Crear objetos QTableWidgetItem y centrar el texto
        item_fecha = QTableWidgetItem(list(self.objeto.historial.keys())[0])
        item_fecha.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
        item_precio = QTableWidgetItem(self.objeto.precio)
        item_precio.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
        font = QFont()
        font.setPointSize(12)  # Tamaño de letra 
        item_fecha.setFont(font)
        item_precio.setFont(font)
        # Insertar elementos en la tabla
        self.tablahist.setItem(0, 0, item_fecha)
        self.tablahist.setItem(0, 1, item_precio)
        print("precio del articulo//", self.objeto.precio)
        print("ruta del articulo//", self.objeto.ruta)
        
        #img
        ruta_carpeta_img = "tracking/imagenes/" + self.objeto.ruta
        print(ruta_carpeta_img)
        print("url del articulo//", self.objeto.url)
        self.lbproducto.setStyleSheet("background-color: transparent;")

        if path.exists(ruta_carpeta_img):
            pixmap = QPixmap(ruta_carpeta_img)
            pixmap_ajustada = pixmap.scaled(self.lbproducto.size(), Qt.AspectRatioMode.KeepAspectRatio)
            self.lbproducto.setPixmap(pixmap_ajustada)
            self.lbproducto.setAlignment(Qt.AlignmentFlag.AlignCenter)
    
    def sitio_web(self):
        confirmacion = QMessageBox.information(self, "Confirmación", "Serás redirigido al sitio web oficial",
                                            QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Cancel)
        if confirmacion == QMessageBox.StandardButton.Ok:
            url = QUrl(self.objeto.url)
            QDesktopServices.openUrl(url)   

    def notificacion(self):
        precio = self.textalerta.text()
            
        if precio:
            self.lbnoti.setText("¡Alerta guardada!")
            self.lbnoti.show()
            self.textalerta.clear()
            # Reproducir un sonido
            sonido_path = "Interfaz/correct.mp3"  
            pygame.mixer.music.load(sonido_path)
            pygame.mixer.music.play()
            QTimer.singleShot(2000, self.lbnoti.hide)
        else:
            QMessageBox.warning(self, "Advertencia", "Por favor, ingrese la cantidad de dinero para activar la alerta")
            
def ejecutar():
    app = QApplication(sys.argv)

    #Creacion de ventanas
    global mainWin
    splash = Splash()
    mainWin = MainWindow()
    thirdWin1 = tienda(["interfaz/gui/imagenes/imgp/GMG.png","tracking_spider_GMG","gallo"],"Interfaz/gui/imagenes/imgp/GMG2.png")
    thirdWin2 = tienda(["interfaz/gui/imagenes/imgp/sycom.png","tracking_sycom","sycom"],"Interfaz/gui/imagenes/imgp/sycim.png")
    thirdWin3 = tienda(["interfaz/gui/imagenes/imgp/Jetstereo.png","tracking_spider_jetstereo","jetstereo"],"Interfaz/gui/imagenes/imgp/Jets.png")
    thirdWin4 = tienda(["interfaz/gui/imagenes/imgp/diun.png","tracking_diunsa","diunsa"],"Interfaz/gui/imagenes/imgp/diu.jpg")
    thirdWin5 = tienda(["interfaz/gui/imagenes/imgp/LadyLee.png","tracking_ladylee","ladylee"],"Interfaz/gui/imagenes/imgp/ld.jpg")
    thirdWin6 = tienda(["interfaz/gui/imagenes/imgp/Radioshack.png","tracking_radioshack","radioshack"],"Interfaz/gui/imagenes/imgp/rad.png")

    
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