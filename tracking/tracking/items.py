import scrapy


class Producto(scrapy.Item):
    url = scrapy.Field()
    tienda = scrapy.Field()
    nombre = scrapy.Field()
    precio = scrapy.Field()
    file_urls = scrapy.Field()
    files = scrapy.Field()
    
