import scrapy
import json

class SaturnLinkSpider(scrapy.Spider):
    name = 'saturn_link'
    # allowed_domains = ['saturn.de']
    # start_urls = ['http://saturn.de/']
    proxy_us = "http://scraperapi.country_code=de:a6438ab03fee3e0af7053fbbcaa5c20c@proxy-server.scraperapi.com:8001"
    headers = {
                # 'Host':'www.mediamarkt.de',
                # 'Pragma':'no-cache',
                # 'Proxy-Authorization':'Basic Lmh4QDQ0MjM1Nzk7aW4uOjY1ZjU1cFFnL2xBaUxwWU9tSys4dTV4TVVheTZjQmZzUkx3d2dmbzFaM2c9',
                'Upgrade-Insecure-Requests':'1',
                'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:84.0) Gecko/20100101 Firefox/84.0'
            }
    def start_requests(self):
        prd_ids = [241042,468906,241041]
        for prd in prd_ids: 
            new_url = "https://www.saturn.de/api/v1/graphql?operationName=CategoryV4&variables=%7B%22hasMarketplace%22%3Afalse%2C%22wcsId%22%3A%22"+str(prd)+"%22%2C%22page%22%3A"+str(1)+"%7D&extensions=%7B%22pwa%22%3A%7B%22salesLine%22%3A%22Saturn%22%2C%22country%22%3A%22DE%22%2C%22language%22%3A%22de%22%7D%2C%22persistedQuery%22%3A%7B%22version%22%3A1%2C%22sha256Hash%22%3A%227805a7790a2e518766c5ccf93f4cc70f49f17a2da0d4de9de5f51b2d6e50a5ec%22%7D%7D"
            yield scrapy.Request(url = new_url, callback = self.paging,headers=self.headers,meta={"proxy":self.proxy_us,"prd":prd} )

    def paging(self,response):
        js = json.loads(response.text)
        count = js["data"]["categoryV4"]["paging"]["pageCount"]
        for i in range(1,int(count)+1):
            new_url = "https://www.saturn.de/api/v1/graphql?operationName=CategoryV4&variables=%7B%22hasMarketplace%22%3Afalse%2C%22wcsId%22%3A%22"+str(response.meta["prd"])+"%22%2C%22page%22%3A"+str(i)+"%7D&extensions=%7B%22pwa%22%3A%7B%22salesLine%22%3A%22Saturn%22%2C%22country%22%3A%22DE%22%2C%22language%22%3A%22de%22%7D%2C%22persistedQuery%22%3A%7B%22version%22%3A1%2C%22sha256Hash%22%3A%227805a7790a2e518766c5ccf93f4cc70f49f17a2da0d4de9de5f51b2d6e50a5ec%22%7D%7D"
            yield scrapy.Request(url = new_url, callback = self.list_page,headers=self.headers,meta={"proxy":self.proxy_us} )
    
    def list_page(self,response):
        js = json.loads(response.text)
        for url in js["data"]["categoryV4"]["products"]:
            yield{
                "link" : response.url,
                "url" : url["details"]["seoUrl"]
            }
