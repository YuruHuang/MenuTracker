import json
from datetime import date

import scrapy


class A13PretSpider(scrapy.Spider):
    name = '13_Pret'
    allowed_domains = ['www.pret.co.uk']
    start_urls = ['https://www.pret.co.uk/en-GB/our-menu']

    def parse(self, response):
        all_urls = response.xpath('//a/@href').getall()
        category_urls = [url for url in all_urls if 'products/categories' in url]
        for category_url in category_urls:
            cat_url = 'https://www.pret.co.uk' + category_url
            yield scrapy.Request(url=cat_url, callback=self.parse_category)

    def parse_category(self, response):
        item_urls = response.xpath('//a[@data-testid="product-link"]/@href').getall()
        for item_url in item_urls:
            absolute_url = f'https://www.pret.co.uk' + item_url
            category = response.url.split('/')[-1]
            yield scrapy.Request(url=absolute_url, callback=self.parse_item, meta={'category': category})

    def parse_item(self, response):
        script_data = response.xpath('//script[@id="__NEXT_DATA__"]/text()').get()
        item_json = json.loads(script_data).get('props').get('pageProps').get('product')
        allergens = item_json.get('allergens')
        item_dict = {
            'collection_date': date.today().strftime("%b-%d-%Y"),
            'rest_name': 'Pret A Manger',
            'menu_id': response.request.url.split('/')[-1],
            'menu_section': response.request.meta['category'],
            'item_name': item_json.get('name'),
            'item_description': item_json.get('description'),
            'allergens': [d['label'] for d in allergens],
            'newUntil': item_json.get('newUntil'),
            'ingredients': item_json.get('ingredients'),
            'servingsize': item_json.get('averageWeight'),
            'vegetarian': item_json.get('suitableForVegetarians'),
            'vegan': item_json.get('suitableForVegans'),
            'url': response.request.url
        }
        nutrients = item_json.get('nutritionals')
        for nutrient in nutrients:
            nutrient_name = nutrient[0]['value']
            item_dict.update({nutrient_name + '_100g': nutrient[1]['value'],
                              nutrient_name + '_perserving': nutrient[2]['value']})
        yield item_dict
