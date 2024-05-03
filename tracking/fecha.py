from datetime import datetime

def obtenerFecha():
        fechaActual = datetime.now()
        fechaFormateada = fechaActual.strftime("%d/%m/%Y")
        return fechaFormateada