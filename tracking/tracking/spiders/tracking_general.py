import scrapy
from tracking.items import Producto
import json
from datetime import datetime
from fecha import obtenerFecha

class trackingPrecios(scrapy.Spider):
    name = "tracking_general"
    # allowed_domains = [
    #     "elgallomasgallo.com.hn", "ladylee.net",
    #     "diunsa.hn", "radioshackla.com",
    #     "jetstereo.com","sycomhn.com"
    # ]

    def start_requests(self):
        #para definir la URL del spider ejecutar con el atributo -a url=<url deseada>
        cadena = getattr(self, "url", None)
        urls = cadena.split(",")
        for url in urls:
            yield scrapy.Request(url,self.parse)

    def parse(self, response):
        producto = Producto()
        producto["url"] =  url = response.url

        if "elgallomasgallo" in url:
            producto["nombre"]=response.css("span.base::text").get()
            producto["precio"]=response.css("span.price::text").get()
            producto["tienda"] = "gallo"
            fecha = obtenerFecha()
            producto['historial'] = {fecha:precio}
            #el campo file_urls almacena las url de las imagenes a descargar
            producto["file_urls"]=[response.css("img.gallery-placeholder__image::attr(src)").get()] # GMG usa imagenes formato .jpg

        elif "sycomhn" in url:
            producto["nombre"]=response.css("h1.product-title.product_title.entry-title::text").get()
            temp =response.css("bdi::text").getall()
            producto["precio"] = temp[1]
            producto["tienda"] = "sycom"
            fecha = obtenerFecha()
            producto['historial'] = {fecha:precio}
            #el campo file_urls almacena las url de las imagenes a descargar
            producto["file_urls"]=[response.css("div.woocommerce-product-gallery__image.slide.first > a::attr(href)").get()] # Sycom usa imagenes formato .png
        
        elif "jetstereo" in url:
            producto["nombre"]=response.css("h1.product-page-title.m-1-::text").get()
            producto["precio"]=response.css("p.salePrice::text").get()
            producto["tienda"] = "jetstereo"
            fecha = obtenerFecha()
            producto['historial'] = {fecha:precio}
            #temp almacena la respuesta del selector "#__NEXT_DATA__::text" en formato json
            temp=json.loads(response.css("#__NEXT_DATA__::text").get())
            #ruta de acceso a la url de la imagen de producto en jetstereo
            cadena = temp["props"]["pageProps"]["product"]["mainImage"]["full"]
            #el campo file_urls almacena las url de las imagenes a descargar
            producto["file_urls"]= [cadena] #jetstereo usa imagenes formato .webp

        elif "diunsa" in url:
            precio = ""
            producto["nombre"]=response.css("span.vtex-store-components-3-x-productBrand::text").get()
            lista=response.css("span.vtex-product-price-1-x-sellingPriceValue > span.vtex-product-price-1-x-currencyContainer > span::text").getall()
            for i in lista:
                precio += i 
            producto["precio"] = precio
            producto["tienda"] = "diunsa"
            fecha = obtenerFecha()
            producto['historial'] = {fecha:precio}
            #el campo file_urls almacena las url de las imagenes a descargar
            producto["file_urls"]=[response.css("img.vtex-store-components-3-x-productImageTag.vtex-store-components-3-x-productImageTag--main::attr(src)").get()] # Diunsa usa imagenes formato .webp
        
        elif "ladylee" in url:
            producto["nombre"] = response.css("h2.product-name::text").get()
            producto["precio"] = response.css("h3.price-primary::text").get()
            producto["tienda"] = "ladylee"
            fecha = obtenerFecha()
            producto['historial'] = {fecha:precio}
            #el campo file_urls almacena las url de las imagenes a descargar
            urlcompleta = response.css("figure::attr(style)").get() # Ladylee usa imagenes formato .webp
            producto["file_urls"]=[urlcompleta[21:-2]]
        
        elif "radioshackla" in url:
            producto["nombre"] = response.css("span.base::text").get()
            temp = response.css("span.price::text").getall()
            producto["precio"] = temp[-1]
            producto["tienda"] = "radioshack"
            fecha = obtenerFecha()
            producto['historial'] = {fecha:precio}
            #el campo file_urls almacena las url de las imagenes a descargar
            # urlLarga = response.css('meta[property="og:image"]::attr(content)').get()
            # lista = urlLarga.split("?")
            # producto["file_urls"]=[lista[0]] # Radioshack usa imagenes formato .jpg

        yield producto
