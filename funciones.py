import json
from os import path

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

    with open('tracking/articulos.json','r',encoding='utf-8') as archivoBase:
        base = json.load(archivoBase)
        for i in base:
            if i['tienda'] == tienda:
                articulos.append(i)
    print(articulos)