import scrapy


class A14CaffeneroSpider(scrapy.Spider):
    name = '14_CaffeNero'
    allowed_domains = ['caffenero.com']
    start_urls = ['http://caffenero.com/']

    def parse(self, response):
        pass
