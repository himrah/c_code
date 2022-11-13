# -*- coding: utf-8 -*-
import time
import datetime
import scrapy
from scrapy.http import Request
# import re
import json
# import traceback
import requests
# from lxml import html
# from scrapy import signals
# import xlrd
# import sys
# reload(sys)
# from bs4 import BeautifulSoup
# sys.setdefaultencoding('utf8')
# from scrapy.http import FormRequest

class FrCdiscountSpider(scrapy.Spider):
    name = 'fr_cdiscount'
    allowed_domains = ['cdiscount.com']
    # start_urls = ['http://cdiscount.com/']
    # proxy = 'http://scraperapi:a6438ab03fee3e0af7053fbbcaa5c20c@proxy-server.scraperapi.com:8001'
    proxy = 'http://scraperapi.render=true:a6438ab03fee3e0af7053fbbcaa5c20c@proxy-server.scraperapi.com:8001'
    meta = {
            'proxy': 'http://scraperapi:a6438ab03fee3e0af7053fbbcaa5c20c@proxy-server.scraperapi.com:8001'
        }

    def file_to_array(self,n):
        f = open(n, 'r')
        x = f.read().splitlines()
        f.close()
        return x
    
    def get_data_bw(self,s,sv,ev):
        # import pdb;pdb.set_trace()
        op = ""
        j = s.find(sv)
        if not j == -1:
            k = s.find(ev,j+len(sv))
            if not k == -1:
                op = (s[j+len(sv):k]).strip()
        return op
    
    def start_requests(self):
        cat = "Notebook"
        inp = open("laptop_links.txt","r").read().split("\n")
        # inp = self.file_to_array("input_lap_reamaining.txt")
        for i in inp[:10]:
            yield Request(url=i, callback=self.parse_details,dont_filter = True, meta={'category':cat,"proxy":"http://scraperapi.country_code=fr:a6438ab03fee3e0af7053fbbcaa5c20c@proxy-server.scraperapi.com:8001"}) 
        # for i in range(1,220):
            # url = "https://www.cdiscount.com/ProductListUC.mvc/UpdateJsonPage?page="+str(i)+"&TechnicalForm.SiteMapNodeId=228394&TechnicalForm.DepartmentId=1070992&TechnicalForm.ProductId=&hdnPageType=ProductList&TechnicalForm.ContentTypeId=3&TechnicalForm.SellerId=&TechnicalForm.PageType=PRODUCTLISTER&TechnicalForm.LazyLoading.ProductSheets=False&TechnicalForm.BrandLicenseId=0&SortForm.BrandLicenseSelectedCategoryPath=&SortForm.SelectedSort=PERTINENCE&ProductListTechnicalForm.Keyword=&ProductListTechnicalForm.TemplateName=InLine"
            # yield Request(url, callback=self.parse,dont_filter = True, meta={'category':cat,'proxy':self.proxy})    
        # for i in range(1,194):
            # url = "https://www.cdiscount.com/informatique/ordinateurs-pc-portables/pc-portables/l-1070992-"+str(i)+".html"
            # yield Request(url, callback=self.parse,dont_filter = True, meta={'category':cat})
            
    # def parse(self, response):
    #     json_data = json.loads(response.text)
    #     for i in range(len(json_data["products"])):
    #         if json_data["products"][i]["url"]:
    #             url = json_data["products"][i]["url"]
    #             yield Request(url, callback=self.parse_details, meta={'proxy':self.proxy})
        # import pdb;pdb.set_trace()
        # category = response.meta['category']
        # nodes= response.xpath("//ul[@id='lpBloc']//li//div[@class='prdtBILDetails']//a")
        # import pdb;pdb.set_trace()
        # for node in nodes:
            # import pdb;pdb.set_trace()
            # url = node.xpath(".//@href").get()
            # yield Request(url, callback=self.parse_details, dont_filter = True, meta={'category':category,'proxy':self.proxy})
    
    def parse_details(self, response):
        # import pdb;pdb.set_trace()
        print(response.body)
        blkdata = ' '.join(response.xpath("//div[@id='descContent']//text()|//ul[@class='listebulletpoint']//text()|//div[@id='fpBulletPointReadMore']//text()").getall()).replace("\n"," ").replace("\r"," ").replace("\t"," ").strip()
        
        yield{
                'competitor_list_price':response.xpath("//div[@class='stroken']//text()").get(), 
                'competitor_markdown_price': ''.join(response.xpath(u"//span[contains(@class,'jsMainPrice') and contains(@class,'hideFromPro')]//text()").getall()),
                'competitor_product_id': '',
                'competitor_product_name':response.xpath(u"normalize-space(//h1[@itemprop='name']//text())").get(), 
                'competitor_model':'',
                'competitor_product_url':response.url,
                'competitor_laptop_type': response.xpath(u"normalize-space(//tr//td[contains(string(),'Catégorie')]//parent::td//following-sibling::td//text())").get(),
                'competitor_screen_size': response.xpath(u"//tr//td[contains(string(),'Ecran') and contains(string(),'Taille de ')]//parent::td//following-sibling::td//text()").get(),
                'competitor_operating_system': response.xpath(u"//tr//td[contains(string(),'Système') and contains(string(),'exploitation')]//parent::td//following-sibling::td//text()").get(),
                'competitor_processor_series': response.xpath(u"normalize-space(//tr//td[contains(string(),'Processeur|Fabricant') or contains(string(),'CPU')]//parent::td//following-sibling::td//text())").get(),
                'competitor_processor_model': '',
                'competitor_graphics': response.xpath(u"normalize-space(//tr//td[contains(string(),'Processeur graphique')]//parent::td//following-sibling::td//text())").get(),
                'competitor_harddrive_capacity':response.xpath(u"normalize-space(//tr//td[contains(string(),'Disque dur') or contains(string(),'Stockage principal')]//parent::td//following-sibling::td//text())").get(),
                'competitor_ram_capacity': response.xpath(u"normalize-space(//tr//td[contains(string(),'RAM') and(not(contains(string(),'max')))]//parent::td//following-sibling::td//text())").get(),
                'competitor_touchscreen': ''.join(response.xpath(u"normalize-space(//h3[contains(string(),'Ecran tactile')]//parent::td//following-sibling::td//a//text())").getall()).strip(),
                'competitor_display_resolution': response.xpath(u"normalize-space(//th[contains(string(),'Affichage')]//following::tr//td[contains(string(),'Résolution')]//parent::td//following-sibling::td//text())").get(),
                'competitor_optical_drive': '',
                'competitor_keyboard_backlit':response.xpath(u"//tr//td[contains(string(),'Rétroéclairage du clavier')]//parent::td//following-sibling::td//text()").get(),
                'competitor_warranty': response.xpath(u"normalize-space(//tr//td[contains(string(),'Garantie')]//parent::td//following-sibling::td//text())").get(),
                'seller_name': "",
                'stock':response.xpath(u"//p[@class='fpProductAvailability']//text()").get(),
                'block_data': ' '.join(blkdata.split())
            }