# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.pipelines.files import FilesPipeline
import hashlib
from scrapy.utils.python import to_bytes
from pathlib import Path

class MyPipeline(FilesPipeline):
    def file_path(self, request, response=None, info=None, *, item=None):
        media_guid = hashlib.sha1(to_bytes(request.url)).hexdigest()
        if item["tienda"] == "gallo" or item['tienda'] == "radioshack":
            media_ext = ".jpg"
            print("Paso 5")
        elif item["tienda"] == "diunsa" or item['tienda'] == "ladylee":
            media_ext = ".webp"
        else:
            media_ext = Path(request.url).suffix
        return f"{media_guid}{media_ext}"
