import sys
from datetime import date

import scrapy
from scrapy import Selector
from selenium import webdriver
from browserPath import web_browser_path


class A56LeonSpider(scrapy.Spider):
    name = '56_Leon'
    allowed_domains = ['leon.co']
    start_urls = ['https://leon.co/menu/']

    def __init__(self):
        op = webdriver.ChromeOptions()
        op.add_argument('headless')
        self.driver = webdriver.Chrome(web_browser_path, options=op)

    def parse(self, response):
        self.driver.get(response.url)
        soup = Selector(text=self.driver.page_source)
        items = soup.xpath('//a[@class="menu-grid__item"]/@href').getall()
        self.driver.quit()
        for item in items:
            yield scrapy.Request(url='https://leon.co' + item, callback=self.parse_item)

    def parse_item(self, response):
        nutrition_rows = response.xpath('//div[@class="menu-item__nutrition__item"]')
        nutrition_dict = {}
        for nutrition_row in nutrition_rows:
            header = nutrition_row.xpath('.//p[@class="small"]/b/text()').get()
            value = nutrition_row.xpath('.//p[@class="small text-right"]/text()').get()
            nutrition_dict.update({header: value})
        item_dict = {
            'rest_name': 'Leon',
            'collection_date': date.today().strftime("%b-%d-%Y"),
            'item_name': response.xpath('//div[@class="menu-item__main-info"]/div/h1/text()').get(),
            'item_description': response.xpath('//div[@class="menu-item__main-info"]/div/p[@class="p-top p-btm"]'
                                               '/text()').get(),
            'allergens': response.xpath('//div[@class="menu-item__main-info"]//b['
                                        '@class="menu-item__main-info__allergen"]/text()').getall(),
            'ingredients': response.xpath('normalize-space(//div[@class="menu-item__ingredients"]/p/text())'
                                          '').get()
        }
        item_dict.update(nutrition_dict)
        yield item_dict
