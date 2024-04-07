import os

print("Pegue una URL")
url = input("")

#cambia la consola a la ruta del archivo actual y ejecuta el spider
os.system("cd "+ os.path.dirname(os.path.abspath(__file__)) + "/tracking" +" && scrapy crawl tracking_spider_jetstereo -o precio.jsonl -a url="+url)


