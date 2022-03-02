from datetime import date

import scrapy


class A38ItsuSpider(scrapy.Spider):
    name = '38_Itsu'
    allowed_domains = ['www.itsu.com']
    start_urls = ['https://www.itsu.com/menu']

    def parse(self, response):
        items = response.xpath('//div[@class="m__menu-item-wrapper"]/a/@href').getall()
        menu_section = response.request.url.split('/')[-2]
        for item in items:
            yield scrapy.Request(url=item, callback=self.parse_item, meta={'menu_section': menu_section})

    def parse_item(self, response):
        yield {
            'item_name': response.xpath('//h1[@class="header-title"]/text()').get(),
            'item_description': response.xpath('//div[@class="m__item-description"]//p/text()').get(),
            'rest_name': 'Itsu',
            'collection_date': date.today().strftime("%b-%d-%Y"),
            'menu_section': response.request.meta['menu_section'],
            'kcal': response.xpath(
                '//div[@class="m__item-nutrition"]//p[contains(text(),"calories")]/following-sibling::h5/text()').get(),
            'fat': response.xpath(
                '//div[@class="m__item-nutrition"]//p[contains(text(),"fat total")]/following-sibling::h5/text()').get(),
            'satfat': response.xpath(
                '//div[@class="m__item-nutrition"]//p[contains(text(),"fat saturated")]/following-sibling::h5/text()').get(),
            'protein': response.xpath(
                '//div[@class="m__item-nutrition"]//p[contains(text(),"protein")]/following-sibling::h5/text()').get(),
            'carb': response.xpath(
                '//div[@class="m__item-nutrition"]//p[contains(text(),"carbs")]/following-sibling::h5/text()').get(),
            'sugar': response.xpath(
                '//div[@class="m__item-nutrition"]//p[contains(text(),"sugars")]/following-sibling::h5/text()').get(),
            'fibre': response.xpath(
                '//div[@class="m__item-nutrition"]//p[contains(text(),"fibre")]/following-sibling::h5/text()').get(),
            'salt': response.xpath(
                '//div[@class="m__item-nutrition"]//p[contains(text(),"salt")]/following-sibling::h5/text()').get(),
            'allergen': response.xpath('//div[@class="allergen-table"]/span/text()').getall()
        }
