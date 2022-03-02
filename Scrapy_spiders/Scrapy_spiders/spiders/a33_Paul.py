import re
from datetime import date

import scrapy


class A33PaulSpider(scrapy.Spider):
    name = '33_Paul'
    allowed_domains = ['www.paul-uk.com']
    start_urls = ['https://www.paul-uk.com']

    def parse(self, response):
        cat_links = response.xpath('//nav//li[contains(@class, "category-item")]/a/@href').getall()
        for cat_link in cat_links:
            yield scrapy.Request(url=cat_link, callback=self.parse_cat)

    def parse_cat(self, response):
        items = response.xpath('//li[@class="item product product-item"]')
        for item in items:
            url_item = item.xpath('.//a/@href').get()
            yield scrapy.Request(url=url_item, callback=self.parse_item)
        next_page = response.xpath('//a[@class="action  next"]/@href')
        if next_page:
            absolute_url = next_page.get()
            yield scrapy.Request(absolute_url, callback=self.parse_cat)

    def parse_item(self, response):
        servingsize = re.findall('[0-9]+',
                                 response.xpath('//div[@class="nutritional-title hide-desk"][1]/text()').get())
        nutrients_100 = response.xpath('//ul[@class="hide-desk"]/li/text()').getall()
        nutrient_dict_100 = {}
        for i in range(len(nutrients_100)):
            nutrient_name = nutrients_100[i] + '_100g'
            value_temp = response.xpath(
                f'//ul[@class="hide-desk"]/li/parent::ul/following-sibling::ul/li[{i + 1}]/text()').get()
            nutrient_dict_100.update({nutrient_name: value_temp})
        nutrients_serving = response.xpath(
            '//div[@class="nutritional-title hide-desk"][1]/following-sibling::ul[1]/li/text()').getall()
        nutrient_dict = {}
        for i in range(len(nutrients_serving)):
            value_temp = response.xpath(
                f'//div[@class="nutritional-title hide-desk"][1]/following-sibling::ul[2]/li[{i + 1}]/text()').get()
            nutrient_dict.update({nutrients_serving[i]: value_temp})
        # values =  response.xpath('//ul[@class="hide-desk"]/li/parent::ul/following-sibling::ul/li/text()').getall()
        # nutrients_dict = dict(zip(nutrients, values))
        allergens = response.xpath('//div[@id="allergens.present"]//ul[1]/li/text()').getall()
        allergen_values = [text.strip() for text in
                           response.xpath('//div[@id="allergens.present"]//ul[2]/li/text()').getall()]
        allergens_dict = dict(zip(allergens, allergen_values))
        item_dict = {
            'collection_date': date.today().strftime("%b-%d-%Y"),
            'rest_name': 'PAUL',
            'item_name': response.xpath('//div[@class="page-title-wrapper"]/h1/text()').get(),
            'item_desc': response.xpath('//div[@itemprop="description"]/text()').get(),
            'price': response.xpath('//span[@class="price"]/text()').get(),
            'allergen': allergens_dict,
            'servingsize': servingsize
        }
        item_dict.update(nutrient_dict)
        item_dict.update(nutrient_dict_100)
        yield item_dict
