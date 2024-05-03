import json
from os import path, system
from datetime import datetime

class Producto:
    def __init__(self,articulo,precio, ruta="", url="",historial={}):
        self.articulo = articulo
        self.precio = precio
        self.ruta = ruta #de la imagen
        self.url = url
        self.historial = historial

def guardarTracker():
    if path.getsize('tracking/articulos.json') > 0:
        with open('tracking/articulos.json','r',encoding='utf-8') as archivoBase:
            base = json.load(archivoBase)
    else:
        base = []
    if path.getsize('tracking/temp.json') == 0:
        return
    with open('tracking/temp.json','r',encoding='utf-8') as temp:
        anexo = json.load(temp)
    
    if len(anexo) == 0:
        return
    
    if filtrarDuplicados(anexo):
        base.append(anexo[0])

        with open('tracking/articulos.json','w',encoding='utf-8') as archivoBase:
            json.dump(base,archivoBase)

def actualizar(obj):
    tienda = obj.nombreTienda
    articulos = []
    productos=[]

    if path.getsize('tracking/articulos.json') == 0:
        return []

    with open('tracking/articulos.json','r',encoding='utf-8') as archivoBase:
        if path.getsize('tracking/articulos.json') == 0:
            return
        base = json.load(archivoBase)

    for i in base:
        if i['tienda'] == tienda:
            articulos.append(i)

    for i in articulos:
        productos.append(Producto(i['nombre'],i['precio'],i['files'][0]["path"],i['url'],i["historial"])) 
    return productos

def borrar(obj,lista):
    #Pendiente de ejecutar y corregir
    tienda=obj.nombreTienda
    nuevaBase=[]

    with open("tracking/articulos.json","r",encoding='utf-8') as articulos:
        base = json.load(articulos)

    for articulo in base:
        if articulo['tienda'] == tienda and articulo['nombre'] in lista:
            continue
        nuevaBase.append(articulo)

    with open("tracking/articulos.json","w",encoding='utf-8') as escritura:
        json.dump(nuevaBase,escritura)

def archivoActual():
    with open('tracking/temp.json','r',encoding='utf-8') as temp:
        cade=json.load(temp)
    return(cade[0]['files'][0]['path'])

def vaciar():
    with open('tracking/temp.json','w',encoding='utf-8') as temp:
        temp.write('')

def filtrarDuplicados(anexo):
    if path.getsize('tracking/articulos.json') == 0:
        return True
    with open('tracking/articulos.json','r',encoding='utf-8') as archivo:
        base = json.load(archivo)
    if anexo[0] in base:
        return False
    return True

def actGeneral():
    urls = ""
    if path.getsize('tracking/articulos.json') == 0:
        return
    with open('tracking/articulos.json','r',encoding='utf-8') as archivo:
        base = json.load(archivo)
    for articulo in base:
        if "radioshackla" not in articulo['url']:
            urls += articulo['url']+","
    urls = urls[0:-1]
    system("cd "+ path.dirname(path.abspath(__file__)) + "/tracking && scrapy crawl tracking_general -O temp.json -a url="+urls)
    #anadirNuevoPrecio()

def anadirNuevoPrecio():
    fechaActual = datetime.now()
    fecha = fechaActual.strftime("%d/%m/%Y")
    with open('tracking/articulos.json','r',encoding='utf-8') as archivo:
        base = json.load(archivo)
    with open('tracking/temp.json','r',encoding='utf-8') as temp:
        anexo = json.load(temp)
    for articuloAnexo in anexo:
        for articuloBase in base:
            if articuloAnexo['url'] == articuloBase['url']:
                print("True")
                if list(articuloAnexo['historial'].keys())[-1]!=list(articuloBase['historial'].keys())[-1]:
                    print(articuloAnexo['historial'], articuloBase['historial'])
                    articuloBase['historial'][fecha] = articuloAnexo['historial'][fecha]
                    print(articuloAnexo['historial'], articuloBase['historial'])
    with open('tracking/articulos.json','w',encoding='utf-8') as escritura:
        json.dump(base,escritura)

    #vaciar()