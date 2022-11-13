import scrapy
import json
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
import codecs
import os
import hashlib
import sys
# reload(sys)
import time
class PontoLinkSpider(CrawlSpider):
    name = 'ponto_link'
    # allowed_domains = ['pontofrio.com.br','pdp-api.pontofrio.com.br']
    user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:87.0) Gecko/20100101 Firefox/87.0"
    # user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36'
    meta = {
            'proxy': 'http://scraperapi:a6438ab03fee3e0af7053fbbcaa5c20c@proxy-server.scraperapi.com:8001'
        }
    def start_requests(self):
        inp = open("input.txt","r").read().split("\n")
        for i in inp:
            # yield scrapy.Request(url='https://www.americanas.com.br/categoria/informatica/notebook/m/samsung?ordenacao=topSelling', headers={
                # 'User-Agent': self.user_agent
            # })
            yield scrapy.Request(url=i,callback=self.crawl_link,meta={"index":1,"json":False},headers={'User-Agent': self.user_agent})
            # yield scrapy.Request(url = i,callback=self.parse_item,headers={'User-Agent': self.user_agent})
    
    def crawl_link(self,response):
        if(response.meta["json"]):
            j = json.loads(response.body)
            if(j["products"]):
                # prd_links = [x["urls"] for x in j["products"]]
                for product in j["products"]:
                    link = product["urls"]
                    yield {"url":link,"cat":response.url}
                    # yield scrapy.Request(url = link,callback=self.parse_item,headers={'User-Agent': self.user_agent})
                next_page = "https://www.pontofrio.com.br/api/catalogo-ssr/products/?{}&PaginaAtual={}&RegistrosPorPagina=20&Platform=1".format(response.url.split("?")[1].split("&")[0],response.meta["index"]+1)
                yield scrapy.Request(url = next_page,callback=self.crawl_link, meta={"index":response.meta["index"]+1,"json":True},headers={'User-Agent': self.user_agent})
        else:
            links = response.xpath("//a[@class='styles__CardMediaWrapper-sc-1gzprri-4 iSxxlY']/@href").extract()
            for link in links:
                yield {"url":link,"cat":response.url}
                # yield scrapy.Request(url = link,callback=self.parse_item,headers={'User-Agent': self.user_agent})

            if(response.xpath("//button[@class='LoadMore__Button-orxhtv-0 jdODqO']")):
                next_page = "https://www.pontofrio.com.br/api/catalogo-ssr/products/?{}&PaginaAtual={}&RegistrosPorPagina=20&Platform=1".format(response.url.split("?")[1],response.meta["index"]+1)
                yield scrapy.Request(url = next_page, callback=self.crawl_link,meta={"index":response.meta["index"]+1,"json":True},headers={'User-Agent': self.user_agent})    


