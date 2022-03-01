from datetime import date

import scrapy


class A27YatesSpider(scrapy.Spider):
    name = '27_Yates'
    allowed_domains = ['tkmenus.com']
    start_urls = ['https://tkmenus.com/greattraditionalpubs']

    def parse(self, response):
        items = response.xpath('//div[@class="k10-l-grid"]')
        for item in items:
            yield {
                'collection_date': date.today().strftime("%b-%d-%Y"),
                'rest_name': "Yate's",
                'menu_section': item.xpath('./ancestor::section[@class="k10-course grid-item"]/h2/text()').get(),
                'item_name': item.xpath('.//span[@class="k10-recipe__name-val"]/text()').get(),
                'item_description': item.xpath('normalize-space(.//p[@class="k10-recipe__desc"]/text())').get(),
                'allergens': [string.strip() for string in
                              item.xpath('.//div[@class="k10-recipe__labels-wrapper-content"]/div/text()').getall()],
                'kcal': item.xpath(
                    './/div[@class="k10-recipe__nutrients-item"]/span[contains(text(),"Energy (kcal)")]/following-sibling::span/text()').get(),
                'kj': item.xpath(
                    './/div[@class="k10-recipe__nutrients-item"]/span[contains(text(),"Energy (kJ)")]/following-sibling::span/text()').get().replace(
                    ',', ''),
                'protein': item.xpath(
                    './/div[@class="k10-recipe__nutrients-item"]/span[contains(text(),"Protein (g)")]/following-sibling::span/text()').get(),
                'carb': item.xpath(
                    './/div[@class="k10-recipe__nutrients-item"]/span[contains(text(),"Carbs (g)")]/following-sibling::span/text()').get(),
                'sugar': item.xpath(
                    './/div[@class="k10-recipe__nutrients-item"]/span[contains(text(),"Sugars (g)")]/following-sibling::span/text()').get(),
                'fat': item.xpath(
                    './/div[@class="k10-recipe__nutrients-item"]/span[contains(text(),"Fat (g)")]/following-sibling::span/text()').get(),
                'satfat': item.xpath(
                    './/div[@class="k10-recipe__nutrients-item"]/span[contains(text(),"Saturates (g)")]/following-sibling::span/text()').get(),
                'salt': item.xpath(
                    './/div[@class="k10-recipe__nutrients-item"]/span[contains(text(),"Salt (g)")]/following-sibling::span/text()').get()
            }
