from datetime import date

import scrapy


class A39BenjerrySpider(scrapy.Spider):
    name = '39_BenJerry'
    allowed_domains = ['www.benjerry.co.uk']
    start_urls = ['https://www.benjerry.co.uk']

    def parse(self, response):
        cat_links = response.xpath('//div[@class="w_bg"]/a/@href').getall()
        for cat_link in cat_links:
            yield scrapy.Request(url='https://www.benjerry.co.uk' + cat_link,
                                 callback=self.parse_page)

    def parse_page(self, response):
        urls = response.xpath('//a[@class="landing-item"]/@data-producturl').getall()
        category = response.request.url.split('/')[-1]
        for url in urls:
            yield scrapy.Request(url='https://www.benjerry.co.uk' + url, callback=self.parse_item,
                                 meta={'cat': category})

    def parse_item(self, response):
        yield {
            'item_name': response.xpath(
                'normalize-space(//h2[@class="productDetails-name h1style"]/text())').get().strip(),
            'collection_date': date.today().strftime("%b-%d-%Y"),
            'rest_name': "Ben & Jerry's",
            'menu_section': response.request.meta['cat'],
            'ingredients': response.xpath('//div[@class="package-ingredients"]/text()').getall(),
            'item_description': response.xpath('//p[@id="productDetails-product_desc-mobile"]/text()').get().strip(),
            'nutrition_url': 'www.benjerry.co.uk' + response.xpath('//img[@class="package-nutrition"]/@src').get()
        }
