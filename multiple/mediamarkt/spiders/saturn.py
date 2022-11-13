import scrapy
import math
import json
import re
from scrapy.http import JsonRequest

class MediamarktSpiderSpider(scrapy.Spider):
    name = 'saturn_crawler'
    proxy_us = "http://scraperapi.country_code=de:a6438ab03fee3e0af7053fbbcaa5c20c@proxy-server.scraperapi.com:8001"
    # proxy
    # allowed_domains = ['mediamarkt.de']
    # start_urls = ['http://mediamarkt.com/']

    def start_requests(self):

        headers = {
            # 'Host':'www.mediamarkt.de',
            # 'Pragma':'no-cache',
            # 'Proxy-Authorization':'Basic Lmh4QDQ0MjM1Nzk7aW4uOjY1ZjU1cFFnL2xBaUxwWU9tSys4dTV4TVVheTZjQmZzUkx3d2dmbzFaM2c9',
            'Upgrade-Insecure-Requests':'1',
            'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:84.0) Gecko/20100101 Firefox/84.0'
        }
        l = open("satran_links.txt").read().split("\n")
        for i in l:
            yield scrapy.Request(url = i, callback = self.description,headers=headers,meta={"proxy":self.proxy_us} )


    # def start_requests(self):


    #     headers = {
    #         # 'Host':'www.mediamarkt.de',
    #         # 'Pragma':'no-cache',
    #         # 'Proxy-Authorization':'Basic Lmh4QDQ0MjM1Nzk7aW4uOjY1ZjU1cFFnL2xBaUxwWU9tSys4dTV4TVVheTZjQmZzUkx3d2dmbzFaM2c9',
    #         'Upgrade-Insecure-Requests':'1',
    #         'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:84.0) Gecko/20100101 Firefox/84.0'
    #     }


    #     # urls = {"22542028":42}
    #     urls = {"241042":459,"468906":105,"241041":252}

    #     # m_url = "https://www.mediamarkt.de/api/v1/graphql?operationName=CategoryV4&variables={%22hasMarketplace%22%3Atrue%2C%22wcsId%22%3A%{}%22%2C%22page%22%3A{}%2C%22experiment%22%3A%22mp%22}&extensions={%22pwa%22%3A{%22salesLine%22%3A%22Media%22%2C%22country%22%3A%22DE%22%2C%22language%22%3A%22de%22}%2C%22persistedQuery%22%3A{%22version%22%3A1%2C%22sha256Hash%22%3A%227805a7790a2e518766c5ccf93f4cc70f49f17a2da0d4de9de5f51b2d6e50a5ec%22}}"
    #     true = True
    #     # m_url = 'https://www.mediamarkt.de/api/v1/graphql?operationName=CategoryV4&variables={"hasMarketplace":true,"wcsId":"{}","page":{},"experiment":"mp"}&extensions={"pwa":{"salesLine":"Media","country":"DE","language":"de"},"persistedQuery":{"version":1,"sha256Hash":"7805a7790a2e518766c5ccf93f4cc70f49f17a2da0d4de9de5f51b2d6e50a5ec"}}'
    #     for url in urls:
    #         last_page = math.ceil(urls[url]/12)

    #         for i in range(1,last_page+1):
    #             print(i)
    #             # new_url = "https://www.mediamarkt.de/api/v1/graphql?operationName=CategoryV4&variables=%7B%22hasMarketplace%22%3Atrue%2C%22wcsId%22%3A%"+url+"%22%2C%22page%22%3A"+str(i)+"%2C%22experiment%22%3A%22mp%22%7D&extensions=%7B%22pwa%22%3A%7B%22salesLine%22%3A%22Media%22%2C%22country%22%3A%22DE%22%2C%22language%22%3A%22de%22%7D%2C%22persistedQuery%22%3A%7B%22version%22%3A1%2C%22sha256Hash%22%3A%227805a7790a2e518766c5ccf93f4cc70f49f17a2da0d4de9de5f51b2d6e50a5ec%22%7D%7D"
    #             # new_url = "https://www.saturn.de/api/v1/graphql?operationName=CategoryV4&variables=%7B%22hasMarketplace%22%3Afalse%2C%22wcsId%22%3A%"+url+"%22%2C%22page%22%3A"+str(i)+"%7D&extensions=%7B%22pwa%22%3A%7B%22salesLine%22%3A%22Saturn%22%2C%22country%22%3A%22DE%22%2C%22language%22%3A%22de%22%7D%2C%22persistedQuery%22%3A%7B%22version%22%3A1%2C%22sha256Hash%22%3A%227805a7790a2e518766c5ccf93f4cc70f49f17a2da0d4de9de5f51b2d6e50a5ec%22%7D%7D"

    #             # new_url = "https://www.saturn.de/api/v1/graphql?operationName=CategoryV4&variables=%7B%22hasMarketplace%22%3Afalse%2C%22wcsId%22%3A%22"+url+"%22%2C%22page%22%"+str(i)+"A3%7D&extensions=%7B%22pwa%22%3A%7B%22salesLine%22%3A%22Saturn%22%2C%22country%22%3A%22DE%22%2C%22language%22%3A%22de%22%7D%2C%22persistedQuery%22%3A%7B%22version%22%3A1%2C%22sha256Hash%22%3A%227805a7790a2e518766c5ccf93f4cc70f49f17a2da0d4de9de5f51b2d6e50a5ec%22%7D%7D"
    #             new_url = "https://www.saturn.de/api/v1/graphql?operationName=CategoryV4&variables=%7B%22hasMarketplace%22%3Afalse%2C%22wcsId%22%3A%22"+url+"%22%2C%22page%22%3A"+str(i)+"%7D&extensions=%7B%22pwa%22%3A%7B%22salesLine%22%3A%22Saturn%22%2C%22country%22%3A%22DE%22%2C%22language%22%3A%22de%22%7D%2C%22persistedQuery%22%3A%7B%22version%22%3A1%2C%22sha256Hash%22%3A%227805a7790a2e518766c5ccf93f4cc70f49f17a2da0d4de9de5f51b2d6e50a5ec%22%7D%7D"
    #             # new_url = "https://www.saturn.de/api/v1/graphql?operationName=CategoryV4&variables=%7B%22hasMarketplace%22%3Afalse%2C%22wcsId%22%3A%22"+url+"%22%2C%22page%2"+str(i)+"%3A2%7D&extensions=%7B%22pwa%22%3A%7B%22salesLine%22%3A%22Saturn%22%2C%22country%22%3A%22DE%22%2C%22language%22%3A%22de%22%7D%2C%22persistedQuery%22%3A%7B%22version%22%3A1%2C%22sha256Hash%22%3A%227805a7790a2e518766c5ccf93f4cc70f49f17a2da0d4de9de5f51b2d6e50a5ec%22%7D%7D"
    #             yield scrapy.Request(url = new_url, callback = self.listPage,headers=headers,meta={"proxy":self.proxy_us} )
    
    def listPage(self,response):
        headers = {
            # 'Host':'www.mediamarkt.de',
            # 'Pragma':'no-cache',
            # 'Proxy-Authorization':'Basic Lmh4QDQ0MjM1Nzk7aW4uOjY1ZjU1cFFnL2xBaUxwWU9tSys4dTV4TVVheTZjQmZzUkx3d2dmbzFaM2c9',
            'Upgrade-Insecure-Requests':'1',
            'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:84.0) Gecko/20100101 Firefox/84.0'
        }        
        # print("---------------------")
        js = json.loads(response.text)
        # print(js["data"]["categoryV4"])
        for url in js["data"]["categoryV4"]["products"]:
            
            # yield scrapy.Request(url = url["details"]["seoUrl"], callback = self.description,headers=headers,meta={"proxy":self.proxy_us} )

            yield{
                "link" : response.url,
                "url" : url["details"]["seoUrl"]
            }
    

    def description(self,response):
        l = []
        laptop_type = screen = os = p_series = p_model = graphics = hdd = ram = touch = resolution = optical = backlit = ""
        main = json.loads(response.xpath("//script[@type='application/ld+json']//text()").get())
        # print("---------------")
        # print(main)
        # print("---------------")
        sku = main["sku"]
        name = main["name"]
        # price = main["offers"]["price"]
        price = "".join(re.findall("price':(.*?),",str(main)))
        mrp = "".join(re.findall('"strikePrice":(.*?),',response.text))
        data = re.search("window.__PRELOADED_STATE__ = (.*?)};",response.text).group(1)
        
        screen = "".join(re.findall('Bildschirmdiagonale \(cm/Zoll\)</span></td><td class="TableCell__StyledDataCell-x5zqr0-0 kvxJLl">(.*?)</td',response.text))

        for i in re.findall('GraphqlProductFeature",(.*?)\}\]',data):
            l.append(json.loads("{"+i+"}]}"))
        
        for i in l:
            if(i.get("name")):
                if(i.get("name") == "Produkttyp"):
                    laptop_type = i.get("value")
                if(i.get("name")== "Bildschirmdiagonale (cm/Zoll)"):
                    screen = i.get("value")
                    # screen "".join(re.findall('Bildschirmdiagonale \(cm/Zoll\)</span></td><td class="TableCell__StyledDataCell-x5zqr0-0 kvxJLl">(.*?)</td',r.text))

                if(i.get("name") == "Betriebssystem"):
                    os = i.get("value")
                if(i.get("name") == "Prozessor"):
                    p_series = i.get("value")
                if(i.get("name")=="Prozessor-Modell"):
                    p_model = i.get("value")
                if(i.get("name")=="Grafikkarte"):
                    graphics = i.get("value")
                if(i.get("name")== "Festplatte 1"):
                    hdd = i.get("value")
                if(i.get("name")=="Arbeitsspeicher-Größe"):
                    ram = i.get("value")
                if(i.get("name") == "Touchscreen"):
                    touch = i.get("value")
                if(i.get("name")=="Bildschirmauflösung"):
                    resolution = i.get("value")
                if(i.get("name") == "Laufwerkstyp"):
                    # 
                    optical = i.get("value")
                if(i.get("name") == "Tastatur"):
                    backlit = i.get("value")
                
        yield{
            "competitor_list_price":price,
            "competitor_markdown_price":mrp,
            "competitor_product_id":sku,
            "competitor_product_name":name,
            "competitor_model":"",
            "competitor_product_url":response.url,
            "competitor_laptop_type":laptop_type,
            "competitor_screen_size":screen,
            "competitor_operating_system":os,
            "competitor_processor_series":p_series,
            "competitor_processor_model":p_model,
            "competitor_graphics":graphics,
            "competitor_harddrive_capacity":hdd,
            "competitor_ram_capacity":ram,
            "competitor_touchscreen":touch,
            "competitor_display_resolution":resolution,
            "competitor_optical_drive":optical,
            "competitor_keyboard_backlit":backlit,
            'competitor_warranty': "",
            'seller_name': "",
            'stock': "",

        }                    


# https://www.saturn.de/api/v1/graphql?operationName=CategoryV4&variables=%7B%22hasMarketplace%22%3Afalse%2C%22wcsId%22%3A%22241042%22%2C%22page%22%3A5%7D&extensions=%7B%22pwa%22%3A%7B%22salesLine%22%3A%22Saturn%22%2C%22country%22%3A%22DE%22%2C%22language%22%3A%22de%22%7D%2C%22persistedQuery%22%3A%7B%22version%22%3A1%2C%22sha256Hash%22%3A%227805a7790a2e518766c5ccf93f4cc70f49f17a2da0d4de9de5f51b2d6e50a5ec%22%7D%7D

# https://www.saturn.de/api/v1/graphql?operationName=CategoryV4&variables={%22hasMarketplace%22%3Afalse%2C%22wcsId%22%3A%22241042%22%2C%22page%22%3A2}&extensions={%22pwa%22%3A{%22salesLine%22%3A%22Saturn%22%2C%22country%22%3A%22DE%22%2C%22language%22%3A%22de%22}%2C%22persistedQuery%22%3A{%22version%22%3A1%2C%22sha256Hash%22%3A%227805a7790a2e518766c5ccf93f4cc70f49f17a2da0d4de9de5f51b2d6e50a5ec%22}}
# https://www.saturn.de/api/v1/graphql?operationName=CategoryV4&variables=%7B%22hasMarketplace%22%3Afalse%2C%22wcsId%22%2A%22241042%22%2C%22page%22%3A3%7D&extensions=%7B%22pwa%22%3A%7B%22salesLine%22%3A%22Saturn%22%2C%22country%22%3A%22DE%22%2C%22language%22%3A%22de%22%7D%2C%22persistedQuery%22%3A%7B%22version%22%3A1%2C%22sha256Hash%22%3A%227805a7790a2e518766c5ccf93f4cc70f49f17a2da0d4de9de5f51b2d6e50a5ec%22%7D%7D                
# https://www.saturn.de/api/v1/graphql?operationName=CategoryV4&variables=%7B%22hasMarketplace%22%3Afalse%2C%22wcsId%22%3A%22241042%22%2C%22page%22%3A2%7D&extensions=%7B%22pwa%22%3A%7B%22salesLine%22%3A%22Saturn%22%2C%22country%22%3A%22DE%22%2C%22language%22%3A%22de%22%7D%2C%22persistedQuery%22%3A%7B%22version%22%3A1%2C%22sha256Hash%22%3A%227805a7790a2e518766c5ccf93f4cc70f49f17a2da0d4de9de5f51b2d6e50a5ec%22%7D%7D
# https://www.saturn.de/api/v1/graphql?operationName=CategoryV4&variables={%22hasMarketplace%22%3Afalse%2C%22wcsId%22%3A%22241042%22%2C%22page%22%3A2}&extensions={%22pwa%22%3A{%22salesLine%22%3A%22Saturn%22%2C%22country%22%3A%22DE%22%2C%22language%22%3A%22de%22}%2C%22persistedQuery%22%3A{%22version%22%3A1%2C%22sha256Hash%22%3A%227805a7790a2e518766c5ccf93f4cc70f49f17a2da0d4de9de5f51b2d6e50a5ec%22}}
