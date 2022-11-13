# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
# import requests
import os
import json
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import xlrd
import time
import hashlib
from bs4 import BeautifulSoup as BS
import codecs
from datetime import date

class GitemSpider(scrapy.Spider):
    name = 'gitem_detail'
    allowed_domains = ['browse.gmarket.co.kr']
    # out = open("links.txt","")
    # start_urls = ['http://auction.kr/']
    # proxy = 'http://scraperapi:a6438ab03fee3e0af7053fbbcaa5c20c@proxy-server.scraperapi.com:8001'
    def __init__(self):
        self.retailer = "gmark"
    
    #function for converting a file to array
    def file_to_array(self,n):
        f = open(n, 'r')
        x = f.read().splitlines()
        f.close()
        return x
        
    def w_t_f(self,fname,mode,enco,str1):
        x = codecs.open(fname,mode,enco)
        x.write(str1)
        x.close
    
    def save_url(self,response):
        c_dir = os.getcwd()
        file_name = c_dir +'/html_desktop/'+ self.url_to_md5(response.url) + '.html'
        page_html = response.text
        f = open(file_name,'w')
        f.write(page_html)
        f.close()
        return file_name

    def url_to_md5(self,url):
        m = hashlib.md5()
        m.update(url)
        return m.hexdigest()
        
        
    def start_requests(self):
        # ar = self.file_to_array("Auction.xlsx")
        # wb = xlrd.open_workbook("gmarket_laptop_missing_url.xlsx") 
        # wb = xlrd.open_workbook("gmark_desktop_urls.xlsx") 
        # wb = xlrd.open_workbook("data_gmarket_laptop_13072020.xlsx") 
        # wb = xlrd.open_workbook("gmarket_desktop_cat_data_26112020.xlsx") 
        # sheet = wb.sheet_by_index(0)
        # rows = sheet.nrows
        # cols = sheet.ncols

        url = "http://browse.gmarket.co.kr/list?category=200001966&t=a&k=32&p={}"
        for i in range(1,201):
            # r = s.get(url.format(i))
            # tree = html.fromstring(r.content)
            # links = tree.xpath("//a[@class='link__item']/@href")

            # for i in links:
                # cat_prod_name = sheet.cell_value(i,0)
                # cat_prod_url = sheet.cell_value(i,1)
                # cat_prod_actual_price = sheet.cell_value(i,2)
                # cat_prod_markdown_price = sheet.cell_value(i,3)
                # cat_prod_discount = sheet.cell_value(i,4)
                # cat_prod_img = sheet.cell_value(i,5)
                # cat_highlights = sheet.cell_value(i,6)
                # cat_page_url = sheet.cell_value(i,7)
                # import pdb;pdb.set_trace()
            yield scrapy.Request(url.format(i),callback=self.parse_link,meta={
                                                            # 'cat_prod_name': cat_prod_name,
                                                            # 'cat_prod_url': cat_prod_url,
                                                            # 'cat_prod_actual_price': cat_prod_actual_price,
                                                            # 'cat_prod_markdown_price': cat_prod_markdown_price,
                                                            # 'cat_prod_discount': cat_prod_discount,
                                                            # 'cat_prod_img': cat_prod_img,
                                                            # 'cat_highlights': cat_highlights,
                                                            # 'cat_page_url': cat_page_url  
                                                            # "cat_page_url":""                                
                                                            },dont_filter=True)
                                                            
    def parse_link(self,response):
        soup = BS(response.body)
        products = soup.find_all("div","box__item-container")
        print("............{}...........".format(len(products)))
        # products = response.xpath("//div[@class='box__item-container']")
        for prd in products:
            link = prd.find("a","link__item").get("href")
            prd_name = prd.find("span","text__item").text
            discount =prd.find("div","box__discount")
            actual = prd.find("div","box__price-seller")
            markdown = prd.find("div","box__price-original")
            cat_img = prd.find("div","box__image").find("img").get("src")
            yield scrapy.Request(link,callback=self.parse,meta={
                                                            'cat_prod_name': prd_name,
                                                            'cat_prod_url': link,
                                                            'cat_prod_actual_price': actual,
                                                            'cat_prod_markdown_price': markdown,
                                                            'cat_prod_discount': discount,
                                                            'cat_prod_img': cat_img,
                                                            'cat_highlights': "",
                                                            'cat_page_url': response.url,
                                                            # "cat_page_url":""
                                                            },dont_filter=True)            



    def parse(self,response):
        # fn = self.save_url(response)
        # stat = response.url + "\t" + fn + "\n"
        # self.w_t_f("stat_gmarket_desktop.txt","a","utf-8",stat)
        # import pdb;pdb.set_trace()
        scc = response.xpath("//script[contains(string(),'brand')]//text()").get()
        if scc:
            json_data = json.loads(scc)
            brand = json_data.get('brand').get('name')			
        else:
            brand = ""
        yield {
            # 'cat_prod_name': response.mata[""],
            # 'cat_prod_url': response.url,
            # 'cat_prod_actual_price': '',
            # 'cat_prod_markdown_price': '',
            # 'cat_prod_discount': response.xpath("//strong[@class='sale']//text()").get(),
            # 'cat_prod_img': response.xpath("//ul[@class='viewer']//li[@class=' on']//img/@src").get(),
            # 'cat_highlights': "",
            # 'cat_page_url': response.meta['cat_page_url'],
            'cat_prod_name': response.meta['cat_prod_name'],
            'cat_prod_url': response.meta['cat_prod_url'],
            'cat_prod_actual_price': response.meta['cat_prod_actual_price'],
            'cat_prod_markdown_price': response.meta['cat_prod_markdown_price'],
            'cat_prod_discount': response.meta['cat_prod_discount'],
            'cat_prod_img': response.meta['cat_prod_img'],
            'cat_highlights': response.meta['cat_highlights'],
            'cat_page_url': response.meta['cat_page_url'],

            'retailer_product_ID': response.xpath("//span[@class='rt']//span[@class='pdnum']//text()").get(),
            'prod_name':response.xpath("//h1[@class='itemtit']//text()").get(),
            'brand':brand,
            
            'prod_actual_price':response.xpath("//strong[@class='price_real']//text()").get(),
            'prod_markdown_price':response.xpath("//span[@class='price_original']//text()").get(),

            # 'prod_actual_price':''.join(response.xpath("//span[@class='price_original']//text()").getall()),
            # 'prod_markdown_price':''.join(response.xpath("//strong[@class='price_real']//text()").getall()),

            
            'prod_discount':response.xpath("//strong[@class='sale']//text()").get(),
            'processor_brand':'',
            'processor_type':'',
            'processor_gen':'',
            'highlights':'',
            'prod_des':'',
            'main_image_urls':'|'.join(response.xpath("//div[contains(@class,'thumb-gallery')]//div[@class='navwrap' or @class='viewerwrap']//li//img//@src").getall()),
            'other_image_urls':"|".join(response.xpath("//div[@id='vip-tab_detail']//div[contains(@class,'box__detail-view')]//img/@src").getall()),
            'time_stamp': time.strftime("%Y-%m-%d %H:%M:%S"),
            'No._of_reviews':''.join(response.xpath("//p[@class='seller-awards']//span[@class='text__review-count']//text()").getall()),
            'Ratings':'',
            'Seller':response.xpath("//p[@class='shoptit']//strong//text()").get()
        }    
