import json
from datetime import date

import scrapy


class A7StarbucksSpider(scrapy.Spider):
    name = '7_Starbucks'
    allowed_domains = ['www.starbucks.co.uk']
    start_urls = ['https://www.starbucks.co.uk/api/v1/menu']

    def parse(self, response):
        categories = json.loads(response.body)
        for cat in categories:
            menu_sections = cat.get('children')
            for menu_section in menu_sections:
                category_name = menu_section.get('elementId')
                item_groups = menu_section.get('children')
                if item_groups[0].get('children'):
                    for item_group in item_groups:
                        items = item_group.get('children')
                        for item in items:
                            yield scrapy.Request(url=item.get('href'), meta={'item_name': item.get('elementId'),
                                                                             'menu_section': category_name,
                                                                             'productid': item.get('productNumber')},
                                                 callback=self.parse_item)
                else:
                    items = item_groups
                    for item in items:
                        yield scrapy.Request(url=item.get('href'), meta={'item_name': item.get('elementId'),
                                                                         'menu_section': category_name,
                                                                         'productid': item.get('productNumber')},
                                             callback=self.parse_item)

    def parse_item(self, response):
        # if len(response.xpath('//dt[@class="nutrition-information-nutritional"]/span[contains(text(),"Serving Size")]'))>0:
        #     servingsizeunit = re.search('\(([^)]+)',response.xpath('//dt[@class="nutrition-information-nutritional"]/span[contains(text(),"Serving Size")]/text()').get()).group(1)
        # else:
        #     servingsizeunit = None
        yield {
            'collection_date': date.today().strftime("%b-%d-%Y"),
            'rest_name': 'Starbucks',
            'menu_section': response.request.meta['menu_section'],
            'item_name': response.xpath('//h2[@class="product-title heading-02 bold"]/text()').get(),
            'menu_id': response.request.meta['productid'],
            'element_id': response.request.meta['item_name'],
            'item_desc': response.xpath('//p[@class="product-description copy-02"]/text()').get(),
            # 'allergen': response.xpath('normalize-space(//div[@class="allergens"]/p/text())').get(),
            # 'ingredients': response.xpath('normalize-space(//div[@class="ingredients"]/p/text())').get(),
            'servingsize': response.xpath(
                '//dt[@class="nutrition-information-nutritional"]/span[contains(text(),"Serving Size")]/following-sibling::span/text()').get(),
            'energy': response.xpath(
                '//dt[@class="nutrition-information-nutritional"]/span[contains(text(),"Energy")]/following-sibling::span/text()').getall(),
            'fat': response.xpath(
                '//dt[@class="nutrition-information-nutritional"]/span[contains(text(),"Fat")]/following-sibling::span/text()').get(),
            'satfat': response.xpath(
                '//dt[@class="nutrition-information-nutritional"]/span[contains(text(),"Saturated Fat")]/following-sibling::span/text()').get(),
            'salt': response.xpath(
                '//dt[@class="nutrition-information-nutritional"]/span[contains(text(),"Salt")]/following-sibling::span/text()').get(),
            'carb': response.xpath(
                '//dt[@class="nutrition-information-nutritional"]/span[contains(text(),"Carbohydrate")]/following-sibling::span/text()').get(),
            'fibre': response.xpath(
                '//dt[@class="nutrition-information-nutritional"]/span[contains(text(),"Fibre")]/following-sibling::span/text()').get(),
            'sugar': response.xpath(
                '//dt[@class="nutrition-information-nutritional"]/span[contains(text(),"Sugar")]/following-sibling::span/text()').get(),
            'protein': response.xpath(
                '//dt[@class="nutrition-information-nutritional"]/span[contains(text(),"Protein")]/following-sibling::span/text()').get(),
            'caffeine': response.xpath(
                '//dt[@class="nutrition-information-nutritional"]/span[contains(text(),"Caffeine (mg)")]/following-sibling::span/text()').get()
            # 'caffeine_range': response.xpath(
            #     '//dt[@class="nutrition-information-nutritional"]/span[contains(text(),"Caffeine Range (mg)")]/following-sibling::span/text()').get(),
        }
