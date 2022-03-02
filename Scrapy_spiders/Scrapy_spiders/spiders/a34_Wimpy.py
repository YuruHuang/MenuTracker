import json
from datetime import date

import scrapy


class A34WimpySpider(scrapy.Spider):
    name = '34_Wimpy'
    allowed_domains = ['wimpy.uk.com']
    start_urls = []

    for i in range(300):
        url = f'https://wimpy.uk.com/api/menu-dish/{i}'
        start_urls.append(url)

    def parse(self, response):
        try:
            resp = json.loads(response.body)
            yield {
                'item_name': resp.get('name'),
                'item_description': resp.get('description'),
                'rest_name': 'Wimpy',
                'collection_date': date.today().strftime("%b-%d-%Y"),
                'item_id': response.request.url.split('/')[-1],
                'carb': resp.get('nutritionals').get('CARBOHYDRATE').get('values').get('PORTION'),
                'carb_100': resp.get('nutritionals').get('CARBOHYDRATE').get('values').get('100G'),
                'kj': resp.get('nutritionals').get('ENERGY_KJ').get('values').get('PORTION'),
                'kj_100': resp.get('nutritionals').get('ENERGY_KJ').get('values').get('100G'),
                'kcal': resp.get('nutritionals').get('ENERGY_KCAL').get('values').get('PORTION'),
                'kcal_100': resp.get('nutritionals').get('ENERGY_KCAL').get('values').get('100G'),
                'fat': resp.get('nutritionals').get('FAT').get('values').get('PORTION'),
                'fat_100': resp.get('nutritionals').get('FAT').get('values').get('100G'),
                'fibre': resp.get('nutritionals').get('FIBRE').get('values').get('PORTION'),
                'fibre_100': resp.get('nutritionals').get('FIBRE').get('values').get('100G'),
                'protein': resp.get('nutritionals').get('PROTEIN').get('values').get('PORTION'),
                'protein_100': resp.get('nutritionals').get('PROTEIN').get('values').get('100G'),
                'salt': resp.get('nutritionals').get('SALT').get('values').get('PORTION'),
                'salt_100': resp.get('nutritionals').get('SALT').get('values').get('100G'),
                'sugar': resp.get('nutritionals').get('SUGAR').get('values').get('PORTION'),
                'sugar_100': resp.get('nutritionals').get('SUGAR').get('values').get('100G'),
                'satfat': resp.get('nutritionals').get('SATURATE').get('values').get('PORTION'),
                'satfat_100': resp.get('nutritionals').get('SATURATE').get('values').get('100G'),
                'allergens': resp.get('allergens')
            }
        except:
            print(i)
