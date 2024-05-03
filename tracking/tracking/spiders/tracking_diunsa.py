import scrapy
from tracking.items import Producto
from datetime import datetime
from fecha import obtenerFecha

class trackingPrecios(scrapy.Spider):
    name = "tracking_diunsa"
    allowed_domains=["diunsa.hn"]

    def start_requests(self):
        #para definir la URL del spider ejecutar con el atributo -a url=<url deseada>
        url = getattr(self, "url", None)
        yield scrapy.Request(url, self.parse)

    def parse(self, response):
        precio = ""
        producto = Producto()
        producto["nombre"]=response.css("span.vtex-store-components-3-x-productBrand::text").get()
        lista=response.css("span.vtex-product-price-1-x-sellingPriceValue > span.vtex-product-price-1-x-currencyContainer > span::text").getall()
        for i in lista:
            precio += i 
        producto["precio"] = precio
        producto["url"] = getattr(self,"url",None)
        producto["tienda"] = "diunsa"
        fecha = obtenerFecha()
        producto['historial'] = {fecha:precio}
        #el campo file_urls almacena las url de las imagenes a descargar
        producto["file_urls"]=[response.css("img.vtex-store-components-3-x-productImageTag.vtex-store-components-3-x-productImageTag--main::attr(src)").get()] # Diunsa usa imagenes formato .webp
        yield producto
    