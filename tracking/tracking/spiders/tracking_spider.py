import scrapy
from tracking.items import Producto
import json

class trackingPrecios(scrapy.Spider):
    name = "tracking_spider_jetstereo"
    #allowed_domains=["jetstereo.com"]

    def start_requests(self):
        #para definir la URL del spider ejecutar con el atributo -a url=<url deseada>
        url = getattr(self, "url", None)
        yield scrapy.Request(url, self.parse)

    def parse(self, response):
        producto = Producto()
        producto["nombre"]=response.css("h1.product-page-title.m-1-::text").get()
        producto["precio"]=response.css("p.salePrice::text").get()
        #producto["file_urls"]= ["https://jet-web.s3.us-west-1.amazonaws.com/images/catalog/public/SELLO%202023_HIS-65A6K.webp"]
        #temp almacena la respuesta del selector "#__NEXT_DATA__::text" en formato json
        temp=json.loads(response.css("#__NEXT_DATA__::text").get())
        #ruta de acceso a la url de la imagen de producto en jetstereo
        cadena = temp["props"]["pageProps"]["product"]["mainImage"]["full"]
        #el campo file_urls almacena las url de las imagenes a descargar
        producto["file_urls"]= [cadena]
        yield producto
