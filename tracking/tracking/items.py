import scrapy


class Producto(scrapy.Item):
    nombre = scrapy.Field()
    precio = scrapy.Field()
    file_urls = scrapy.Field()
    files = scrapy.Field()
    
