import json
import time
import scrapy
from bs4 import BeautifulSoup as BS


class GmarketSpider(scrapy.Spider):
    name = 'gmarket'
    proxy_us = "http://scraperapi.country_code=kr:a6438ab03fee3e0af7053fbbcaa5c20c@proxy-server.scraperapi.com:8001"
    # allowed_domains = ['gmarket.com']
    # start_urls = ['http://gmarket.com/']

    def start_requests(self):
        
    	# f = open("input.txt",'r').read().split("\n")
    	# for i in f:
     #        # print(i)
    	# 	yield scrapy.Request(i,callback=self.parse,meta={"proxy":self.proxy_us})
    	
        
    	url = "http://browse.gmarket.co.kr/list?category=200001966&t=a&k=32&p={}"
    	for i in range(1,201):
    		yield scrapy.Request(url.format(i),callback=self.parse_link,meta={"proxy":self.proxy_us},dont_filter=True)


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
            

            # 'cat_prod_name': response.meta['cat_prod_name'],
            # 'cat_prod_url': response.meta['cat_prod_url'],
            # 'cat_prod_actual_price': response.meta['cat_prod_actual_price'],
            # 'cat_prod_markdown_price': response.meta['cat_prod_markdown_price'],
            # 'cat_prod_discount': response.meta['cat_prod_discount'],
            # 'cat_prod_img': response.meta['cat_prod_img'],
            # 'cat_highlights': response.meta['cat_highlights'],
            # 'cat_page_url': response.meta['cat_page_url'],


            'cat_prod_name': response.xpath("//h1[@class='itemtit']//text()").get(),
            'cat_prod_url': response.url,
            'cat_prod_actual_price': response.xpath("//strong[@class='price_real']//text()").get(),
            'cat_prod_markdown_price': response.xpath("//span[@class='price_original']//text()").get(),
            'cat_prod_discount': response.xpath("//strong[@class='sale']//text()").get(),
            'cat_prod_img': "",
            'cat_highlights': "",
            'cat_page_url': "",



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