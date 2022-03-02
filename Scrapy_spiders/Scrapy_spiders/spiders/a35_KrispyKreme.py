from datetime import date

import scrapy
from scrapy_selenium import SeleniumRequest


class A35KrispycremeSpider(scrapy.Spider):
    name = '35_KrispyKreme'
    allowed_domains = ['www.krispykreme.co.uk']
    start_urls = ['https://www.krispykreme.co.uk/shop.html']

    def parse(self, response):
        urls = response.xpath('//div[@class="product product-item-media"]/figure/a/@href').getall()
        for url in urls:
            yield SeleniumRequest(url=url, callback=self.parse_item, wait_time=10)
        next_page = response.xpath('//a[@class="action  next"]/@href').get()
        if next_page:
            yield scrapy.Request(url=next_page, callback=self.parse)

    def parse_item(self, response):
        yield {
            'item_name': response.xpath('//span[@class="base"]/text()').get(),
            'item_description': response.xpath('//div[@class="product attribute description"]//p/text()').getall(),
            'rest_name': 'Krispy Kreme',
            'collection_date': date.today().strftime("%b-%d-%Y"),
            'kj': response.xpath('//table//td[contains(text(),"Energy (kj)")]/following-sibling::td[1]/text()').get(),
            'kj_100': response.xpath(
                '//table//td[contains(text(),"Energy (kj)")]/following-sibling::td[2]/text()').get(),
            'kcal': response.xpath(
                '//table//td[contains(text(),"Energy (cal)")]/following-sibling::td[1]/text()').get(),
            'kcal_100': response.xpath(
                '//table//td[contains(text(),"Energy (cal)")]/following-sibling::td[2]/text()').get(),
            'fat': response.xpath('//table//td[contains(text(),"Fat - Total")]/following-sibling::td[1]/text()').get(),
            'fat_100': response.xpath(
                '//table//td[contains(text(),"Fat - Total")]/following-sibling::td[2]/text()').get(),
            'satfat': response.xpath(
                '//table//td[contains(text(),"- Saturated")]/following-sibling::td[1]/text()').get(),
            'satfat_100': response.xpath(
                '//table//td[contains(text(),"- Saturated")]/following-sibling::td[2]/text()').get(),
            'carb': response.xpath(
                '//table//td[contains(text(),"Carbohydrates")]/following-sibling::td[1]/text()').get(),
            'carb_100': response.xpath(
                '//table//td[contains(text(),"Carbohydrates")]/following-sibling::td[2]/text()').get(),
            'sugar': response.xpath('//table//td[contains(text(),"- Sugars")]/following-sibling::td[1]/text()').get(),
            'sugar_100': response.xpath(
                '//table//td[contains(text(),"- Sugars")]/following-sibling::td[2]/text()').get(),
            'fibre': response.xpath('//table//td[contains(text(),"Fibre")]/following-sibling::td[1]/text()').get(),
            'fibre_100': response.xpath(
                '//table//td[contains(text(),"Fibre")]/following-sibling::td[2]/text()').get(),
            'protein': response.xpath('//table//td[contains(text(),"Protein")]/following-sibling::td[1]/text()').get(),
            'protein_100': response.xpath(
                '//table//td[contains(text(),"Protein")]/following-sibling::td[2]/text()').get(),
            'salt': response.xpath('//table//td[contains(text(),"Salt")]/following-sibling::td[1]/text()').get(),
            'salt_100': response.xpath(
                '//table//td[contains(text(),"Salt")]/following-sibling::td[2]/text()').get(),
            'allergen': response.xpath('//h4[contains(text(),"Allergens")]/following-sibling::p[1]/text()').get()
        }
