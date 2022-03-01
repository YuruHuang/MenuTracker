import scrapy


class A13PretSpider(scrapy.Spider):
    name = '13_Pret'
    allowed_domains = ['pret.com']
    start_urls = ['http://pret.com/']

    def parse(self, response):
        pass
