import scrapy
from scrapy import Request
from scrapy.http import JsonRequest
import re
import json
import time
import re

class LenovoCrawlerSpider(scrapy.Spider):
    name = 'lenovo_crawler'
    proxy_us = "http://scraperapi.country_code=de:a6438ab03fee3e0af7053fbbcaa5c20c@proxy-server.scraperapi.com:8001"
    # allowed_domains = ['lenovo.com']
    # start_urls = ['http://lenovo.com/']

    # def parse(self, response):
    #     pass
    Super_category = "Electronics"
    Retailer = "Lenovo"
    media_type = "Website"
    market = "Internet"
    Sale_start_date = ""
    Sale_end_date = ""
    page_position = "Category_Page"


    def start_requests(self):
        urls = [

        "https://www.lenovo.com/fi/fi/search/facet/query/v3?ch=-1984127214&categories=DESKTOPS&page={}&pageSize=20&sort=sortBy&currency=EUR",
        "https://www.lenovo.com/fi/fi/search/facet/query/v3?ch=-1503123819&categories=LAPTOPS&page={}&pageSize=20&sort=sortBy&currency=EUR",
        "https://www.lenovo.com/dk/da/search/facet/query/v3?ch=-1869462888&categories=DESKTOPS&page={}&pageSize=20&sort=sortBy&currency=DKK",
        "https://www.lenovo.com/dk/da/search/facet/query/v3?ch=1719637763&categories=LAPTOPS&page={}&pageSize=20&sort=sortBy&currency=DKK",
        "https://www.lenovo.com/ch/de/search/facet/query/v3?ch=-1342807374&categories=LAPTOPS&page={}&pageSize=20&sort=sortBy&currency=CHF",
        "https://www.lenovo.com/ch/de/search/facet/query/v3?ch=1406558228&categories=DESKTOPS&page={}&pageSize=20&sort=sortBy&currency=CHF",
        "https://www.lenovo.com/be/nl/search/facet/query/v3?ch=649607991&categories=DESKTOPS&page={}&pageSize=20&sort=sortBy&currency=EUR",
        "https://www.lenovo.com/be/nl/search/facet/query/v3?ch=-727258103&categories=LAPTOPS&page={}&pageSize=20&sort=sortBy&currency=EUR",
        'https://www.lenovo.com/no/no/search/facet/query/v3?ch=107166879&categories=LAPTOPS&page={}&pageSize=20&sort=sortBy&currency=NOK',
        "https://www.lenovo.com/no/no/search/facet/query/v3?ch=-1498848108&categories=DESKTOPS&page={}&pageSize=20&sort=sortBy&currency=NOK",
        "https://www.lenovo.com/se/sv/search/facet/query/v3?ch=-1384654670&categories=DESKTOPS&page={}&pageSize=20&sort=sortBy&currency=SEK",
        "https://www.lenovo.com/se/sv/search/facet/query/v3?ch=-1312475500&categories=LAPTOPS&page={}&pageSize=20&sort=sortBy&currency=SEK",


        "https://www.lenovo.com/de/de/search/facet/query/v3?ch=1406558228&categories=DESKTOPS&page={}&pageSize=20&sort=sortBy&currency=EUR",
        "https://www.lenovo.com/de/de/search/facet/query/v3?ch=1841299381&categories=LAPTOPS&page={}&pageSize=20&sort=sortBy&currency=EUR",
        "https://www.lenovo.com/fr/fr/search/facet/query/v3?ch=18211177&categories=DESKTOPS&page={}&pageSize=20&sort=sortBy&currency=EUR",
        "https://www.lenovo.com/fr/fr/search/facet/query/v3?ch=961207917&categories=LAPTOPS&page={}&pageSize=20&sort=sortBy&currency=EUR",
        "https://www.lenovo.com/it/it/search/facet/query/v3?ch=-1901387158&categories=DESKTOPS&page={}&pageSize=20&sort=sortBy&currency=EUR",
        "https://www.lenovo.com/it/it/search/facet/query/v3?ch=-1290414803&categories=LAPTOPS&page={}&pageSize=20&sort=sortBy&currency=EUR",
        "https://www.lenovo.com/es/es/search/facet/query/v3?ch=-1198139385&categories=DESKTOPS&page={}&pageSize=20&sort=sortBy&currency=EUR",
        "https://www.lenovo.com/es/es/search/facet/query/v3?ch=1743671682&categories=LAPTOPS&page={}&pageSize=20&sort=sortBy&currency=EUR",
        "https://www.lenovo.com/gb/en/search/facet/query/v3?ch=-1498848108&categories=DESKTOPS&page={}&pageSize=20&sort=sortBy&currency=GBP",
        "https://www.lenovo.com/gb/en/search/facet/query/v3?ch=510284493&categories=LAPTOPS&page={}&pageSize=20&sort=sortBy&currency=GBP",
        "https://www.lenovo.com/nl/nl/search/facet/query/v3?ch=649607991&categories=DESKTOPS&page={}&pageSize=20&sort=sortBy&currency=EUR",
        "https://www.lenovo.com/nl/nl/search/facet/query/v3?ch=-630940297&categories=LAPTOPS&page={}&pageSize=20&sort=sortBy&currency=EUR",


        ]
        
        for url in urls:
            # print(url)
            yield JsonRequest(url = url.format(0),method="GET",callback=self.parse,meta={"url":url,"count":0})

    def parse(self, response):
        js = json.loads(response.text)
        if(js["currentResults"]!=0):
            for i in js["results"]:
                # print("-----------------"+response.url[:28]+i["url"]+"-----------------")
                yield Request(url = response.url[:28]+i["url"],callback=self.parse_D)
                # yield {
                # 	"url":i["url"],
                # 	"link":response.url
                # }
                yield JsonRequest(url = response.meta["url"].format(int(response.meta["count"])+1),method="GET",callback=self.parse,meta={"url":response.meta["url"],"count":int(response.meta["count"])+1})



    def parse_D(self,response):
        # print("......{}.....".format(response.url))
        model_name = response.xpath("normalize-space(//h1[@class='desktopHeader']//text())").get()
        # if "lenovo" in model_name.lower():
            # model_name = "Lenovo " + model_name
        yield {
            'Retailer': "Lenovo",
            'Category_Name': "",
            'Brand': "Lenovo",
            'Retailer_inner': '',
            'Model_Number': response.xpath("//meta[@name='productid']//@content").get(),
            'URL_Link': response.url, 
            'Country': response.url[23:25],
            'chassis': '',
            'Main_Page': '',
            
            'Lenovo_Chassis': '',
            'Navigate_add_to_Cart': '',
            'Model_Name': model_name,
            'Regular_Price': response.xpath("//dd[contains(@class,'pricingSummary-priceList-value')][1]//text()").get(),
            'Sales_Price': response.xpath("//dd[@itemprop='price']//text()").get(),
            'Dollar_Off': '',
            'Processor': response.xpath(u"normalize-space(//li[@data-pn='Processor']//p[contains(@class,'configuratorItem-mtmTable-description')]//text())").get(),
            'OS': response.xpath(u"normalize-space(//li[@data-pn='Operating System']//p[contains(@class,'configuratorItem-mtmTable-description')]//text())").get(),
            'Screen_size': response.xpath(u"normalize-space(//li[@data-pn='Display Type']//p[contains(@class,'configuratorItem-mtmTable-description')]//text())").get(),
            'RAM': response.xpath(u"normalize-space(//li[@data-pn='Memory']//p[contains(@class,'configuratorItem-mtmTable-description')]//text())").get(),
            'Hard_Drive': ' '.join(response.xpath(u"normalize-space(//li[contains(@data-pn,'Hard Drive')]//p[contains(@class,'configuratorItem-mtmTable-description')]//text())").getall()).strip(),
            'Graphics': response.xpath(u"normalize-space(//li[@data-pn='Graphics']//p[contains(@class,'configuratorItem-mtmTable-description')]//text())").get(),
            'Camera': '',
            'Bluetooth': '',
            'Warranty': response.xpath(u"normalize-space(//li[@data-pn='Warranty']//p[contains(@class,'configuratorItem-mtmTable-description')]//text())").get(),
            'Battery': '',
            'Display_Resolution': response.xpath(u"normalize-space(//li[@data-pn='Display Type']//p[contains(@class,'configuratorItem-mtmTable-description')]//text())").get(), 
            'Color': '',
            'Product_details': '',
            'lead_time':response.xpath("//div[contains(@id,'deliveryTimeHolder')]//text()").get(),
            'Date': time.strftime("%Y-%m-%d %H:%M:%S")
        }


    def parse_details(self,response):
        yield{
            'Super_category': self.Super_category,
            'Category': response.xpath("//nav[@class='breadcrumb-wrapper']//span[@itemprop='title']//text()").extract()[1],
            'Retailer': self.Retailer,
            'Brand':"Lenovo",
            'Media_type': self.media_type,
            'Market': self.market,
            'Sale_start_date': self.Sale_start_date,
            'Sale_end_date': self.Sale_end_date,
            'Page_position': self.page_position,
            'Promotion_category':'',
            'Promotion':'',
            'Additional_offers_1':response.xpath("//div[@class='merch-tagLabel-ribbon modelCust__ribbon tagLabel-orange taglabel-font-lg']//text()").get(),
            'Additional_offers_2':'',
            'Model_name': response.xpath("//h1//text()").get(),
            'Model_number':"",
            'SKU':"".join(re.findall('mpn": "(.*?)"',response.text)),
            'MPN':"".join(re.findall('mpn": "(.*?)"',response.text)),
            'Product_description':"".join(response.xpath("//div[@class='hero-productDescription-body mediaGallery-productDescription-body']//text()").extract()).strip(),
            'Promotion_title':'',
            'Ecoupon_code':response.xpath("//span[@class='pricingSummary-couponCode']//text()").get(),
            'Regular_price': response.xpath("//meta[@name='productprice']/@content").get(),#response.meta['rp'],
            'Sales_price': response.xpath("//dd[@itemprop='price']//text()").get(), #response.meta['sp'],
            'Unit_price':'',
            'NOR_price':'',
            'Dollar_off': float(response.xpath("//meta[@name='productprice']/@content").get().replace(".","").replace(",",".").replace(" €","")) - float(response.xpath("//dd[@itemprop='price']//text()").get().replace(".","").replace(",",".").replace(" €","")),
            'Percentage_off':'',
            'Coupon_amount':'',
            'Rebate_amount':'',
            'Gift_card_amount':'',
            'Limit1':'',
            'Adtype':'',
            'MT_value_index':'',
            'Extraction_date':time.strftime("%Y-%m-%d %H:%M:%S"),
            'Product_url_link':response.url,
            'html_content':response.xpath("//div[@class='pageWrapper']").extract()

    
        }

