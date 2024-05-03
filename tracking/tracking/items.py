import scrapy


class Producto(scrapy.Item):
    nombre = scrapy.Field()
    precio = scrapy.Field()
    url = scrapy.Field()
    tienda = scrapy.Field()
    file_urls = scrapy.Field()
    files = scrapy.Field()
    historial = scrapy.Field()
    
