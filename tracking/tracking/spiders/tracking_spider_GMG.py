import scrapy
from tracking.items import Producto
from fecha import obtenerFecha

class trackingPrecios(scrapy.Spider):
    name = "tracking_spider_GMG"
    allowed_domains=["elgallomasgallo.com.hn"]

    def start_requests(self):
        #para definir la URL del spider ejecutar con el atributo -a url=<url deseada>
        url = getattr(self, "url", None)
        yield scrapy.Request(url, self.parse)

    def parse(self, response):
        producto = Producto()
        producto["nombre"]=response.css("span.base::text").get()
        producto["precio"]=response.css("span.price::text").get()
        producto["url"] = getattr(self,"url",None)
        producto["tienda"] = "gallo"
        fecha = obtenerFecha()
        producto['historial'] = {fecha:producto['precio']}
        #el campo file_urls almacena las url de las imagenes a descargar
        producto["file_urls"]=[response.css("img.gallery-placeholder__image::attr(src)").get()] # GMG usa imagenes formato .jpg
        yield producto