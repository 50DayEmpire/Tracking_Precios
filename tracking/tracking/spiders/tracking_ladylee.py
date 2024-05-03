import scrapy
from tracking.items import Producto
from fecha import obtenerFecha

class trackingPrecios(scrapy.Spider):
    name = "tracking_ladylee"
    allowed_domains=["ladylee.net"]

    def start_requests(self):
        #para definir la URL del spider ejecutar con el atributo -a url=<url deseada>
        url = getattr(self, "url", None)
        yield scrapy.Request(url, self.parse)

    def parse(self, response):
        producto = Producto()
        producto["nombre"] = response.css("h2.product-name::text").get()
        producto["precio"] = response.css("h3.price-primary::text").get()
        producto["url"] = getattr(self,"url",None)
        producto["tienda"] = "ladylee"
        fecha = obtenerFecha()
        producto['historial'] = {fecha:producto['precio']}
        #el campo file_urls almacena las url de las imagenes a descargar
        url = response.css("figure::attr(style)").get() # Ladylee usa imagenes formato .webp
        producto["file_urls"]=[url[21:-2]]
        yield producto