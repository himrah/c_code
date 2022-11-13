import scrapy


class SaturnSpiderSpider(scrapy.Spider):
    name = 'saturn_spider'
    allowed_domains = ['saturn.de']
    start_urls = ['http://saturn.de/']

    def parse(self, response):
        pass
