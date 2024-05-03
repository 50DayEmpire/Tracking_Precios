import scrapy
from tracking.items import Producto
from fecha import obtenerFecha

class trackingPrecios(scrapy.Spider):
    name = "tracking_radioshack"
    #allowed_domains=["radioshackla.com"]
    custom_settings={
       "ROBOTSTXT_OBEY" : "False"
    }

    def start_requests(self):
        #para definir la URL del spider ejecutar con el atributo -a url=<url deseada>
        url = getattr(self, "url", None)
        yield scrapy.Request(url, self.parse)

    def parse(self, response):
        producto = Producto()
        producto["nombre"] = response.css("span.base::text").get()
        temp = response.css("span.price::text").getall()
        producto["precio"] = temp[-1]
        producto["url"] = getattr(self,"url",None)
        producto["tienda"] = "radioshack"
        fecha = obtenerFecha()
        producto['historial'] = {fecha:temp[-1]}
        #el campo file_urls almacena las url de las imagenes a descargar
        urlLarga = response.css('meta[property="og:image"]::attr(content)').get()
        lista = urlLarga.split("?")
        producto["file_urls"]=[lista[0]] # Radioshack usa imagenes formato .jpg
        yield producto