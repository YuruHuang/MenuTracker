import scrapy


class A15WagamamaSpider(scrapy.Spider):
    name = '15_wagamama'
    allowed_domains = ['wagamama.com']
    start_urls = ['http://wagamama.com/']

    def parse(self, response):
        pass
