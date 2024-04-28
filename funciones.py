import json
from os import path

class Producto:
    def __init__(self,articulo,precio):
        self.articulo = articulo
        self.precio = precio

def guardarTracker():
    if path.getsize('tracking/articulos.json') > 0:
        with open('tracking/articulos.json','r',encoding='utf-8') as archivoBase:
            base = json.load(archivoBase)
    else:
        base = []

    with open('tracking/temp.json','r',encoding='utf-8') as temp:
        anexo = json.load(temp)
    
    if len(anexo) != 0:
        base.append(anexo[0])

        with open('tracking/articulos.json','w',encoding='utf-8') as archivoBase:
            json.dump(base,archivoBase)

def actualizar(obj):
    tienda = obj.nombreTienda
    articulos = []
    productos=[]

    with open('tracking/articulos.json','r',encoding='utf-8') as archivoBase:
        if path.getsize('tracking/articulos.json') == 0:
            return
        base = json.load(archivoBase)

    for i in base:
        if i['tienda'] == tienda:
            articulos.append(i)

    for i in articulos:
        productos.append(Producto(i['nombre'],i['precio'])) 
    return productos

def borrar(obj):
    tienda=obj.nombreTienda

    with open("tracking/articulos.json") as articulos:
        base = json.load(articulos)
    

def archivoActual():
    with open('tracking/temp.json','r',encoding='utf-8') as temp:
        cade=json.load(temp)
    return(cade[0]['files'][0]['path'])

def vaciar():
    with open('tracking/temp.json','w',encoding='utf-8') as temp:
        temp.write('')
