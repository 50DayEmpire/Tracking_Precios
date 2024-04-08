import os
print("""
1. Jetstereo
2. Gallo mas Gallo
""")
n=int(input())
print("Pegue una URL")
url = input("")

#cambia la consola a la ruta del archivo actual y ejecuta el spider

if n==1:
    os.system("cd "+ os.path.dirname(os.path.abspath(__file__)) + "/tracking" +" && scrapy crawl tracking_spider_jetstereo -o precio.jsonl -a url="+url)
elif n==2:
    os.system("cd "+ os.path.dirname(os.path.abspath(__file__)) + "/tracking" +" && scrapy crawl tracking_spider_GMG -o precio.jsonl -a url="+url)