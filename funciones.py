import json
from os import path

class Producto:
    def __init__(self,articulo,precio):
        self.articulo = articulo
        self,precio = precio

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
    n=0

    with open('tracking/articulos.json','r',encoding='utf-8') as archivoBase:
        if path.getsize('tracking/articulos.json') == 0:
            return
        base = json.load(archivoBase)
        for i in base:
            if i['tienda'] == tienda:
                articulos.append(i)
    for i in articulos:
        productos[n] = Producto(i[0],i[1])
        n+=1
    print(productos)

def borrar(obj):
    tienda=obj.nombreTienda