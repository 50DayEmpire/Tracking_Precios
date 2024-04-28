import scrapy
from tracking.items import Producto

class trackingPrecios(scrapy.Spider):
    name = "tracking_sycom"
    allowed_domains=["sycomhn.com"]

    def start_requests(self):
        #para definir la URL del spider ejecutar con el atributo -a url=<url deseada>
        url = getattr(self, "url", None)
        yield scrapy.Request(url, self.parse)

    def parse(self, response):
        producto = Producto()
        producto["nombre"]=response.css("h1.product-title.product_title.entry-title::text").get()
        temp =response.css("bdi::text").getall()
        producto["precio"] = temp[1]
        producto["url"] = getattr(self,"url",None)
        producto["tienda"] = "sycom"
        #el campo file_urls almacena las url de las imagenes a descargar
        producto["file_urls"]=[response.css("div.woocommerce-product-gallery__image.slide.first > a::attr(href)").get()] # Sycom usa imagenes formato .png
        yield producto