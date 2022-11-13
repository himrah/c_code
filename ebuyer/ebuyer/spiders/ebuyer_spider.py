import scrapy
from scrapy import Request
import time

class EbuyerSpiderSpider(scrapy.Spider):
    name = 'ebuyer_spider'
    allowed_domains = ['ebuyer.com']
    proxy_us = "http://scraperapi.country_code=us:a6438ab03fee3e0af7053fbbcaa5c20c@proxy-server.scraperapi.com:8001"
    # start_urls = ['http://ebuyer.com/']

    Super_category = "Electronics"
    Retailer = "Ebuyer"
    media_type = "Website"
    market = "Internet"
    Sale_start_date = ""
    Sale_end_date = ""
    page_position = "Category_Page"



    def start_requests(self):
        urls = ["https://www.ebuyer.com/store/Computer/cat/Laptops","https://www.ebuyer.com/store/Computer/cat/Desktop-PC"]
        for url in urls:
            yield Request(url, meta={"proxy":self.proxy_us}, callback=self.parse)        

    def parse(self, response):
        detail_urls = ["https://www.ebuyer.com"+i for i in response.xpath("//div[@class='grid-item js-listing-product']//h3//a/@href").extract()]
        for url in detail_urls:
            yield Request(url, meta={"proxy":self.proxy_us}, callback=self.parse_detail)
        
        next_page_url = "".join(set(response.xpath("//li[@class='pagination__item next-page']//a/@href").extract()))
        
        if(next_page_url):
            yield Request(response.urljoin(next_page_url), meta={"proxy":self.proxy_us}, callback=self.parse)
    

    def parse_detail(self,response):

        if(response.xpath("//div[@class='purchase-info__price']//div[@class='inc-vat']//span[@class='saving']//text()").get()):
            dollr_saving = "".join(response.xpath("//div[@class='purchase-info__price']//div[@class='inc-vat']//span[@class='saving']//text()").get()).replace("save ","")
        else:
            dollr_saving =""
            
        yield{
            'Super_category': self.Super_category,
            'Category': response.xpath("//div[@class='breadcrumb js-breadcrumb']//a//text()")[-2].extract().strip(),
            'Retailer': self.Retailer,
            'Brand':response.xpath("//div[@class='product-hero__mfr']//img/@alt").get(),
            'Media_type': self.media_type,
            'Market': self.market,
            'Sale_start_date': self.Sale_start_date,
            'Sale_end_date': self.Sale_end_date,
            'Page_position': self.page_position,
            'Promotion_category':'',
            'Promotion':'',
            'Additional_offers_1':'',
            'Additional_offers_2':'',
            'Model_name': response.xpath("//h1[@class='product-hero__title']//text()").get(),
            'Model_number':"",
            'SKU':response.xpath("//span[@class='mfr']//text()").get().replace("Mfr part code: ",""),
            'MPN':'',
            'Product_description':" ".join(response.xpath("//div[@id='product-desc-section']//text()").extract()).strip(),
            'Promotion_title':'',
            'Ecoupon_code':'',
            'Regular_price': response.xpath("//div[@class='purchase-info__price']//div[@class='inc-vat']//span[@class='was']//text()").get(),#response.meta['rp'],
            'Sales_price': "".join(response.xpath("//div[@class='purchase-info__price']//div[@class='inc-vat']//p[@class='price']//text()").extract()).replace("\n","").replace("\xa0","").strip().replace(" ","").replace("inc.vat",""), #response.meta['sp'],
            'Unit_price':'',
            'NOR_price':'',
            'Dollar_off':dollr_saving,
            'Percentage_off':'',
            'Coupon_amount':'',
            'Rebate_amount':'',
            'Gift_card_amount':'',
            'Limit1':'',
            'Adtype':'',
            'MT_value_index':'',
            'Extraction_date':time.strftime("%Y-%m-%d %H:%M:%S"),
            'Product_url_link':response.url,   
            'html_content':"",
        }     
