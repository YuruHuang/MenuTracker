import json
from datetime import date

import scrapy


class A41BenugoSpider(scrapy.Spider):
    name = '42_Benugo'
    allowed_domains = ['www.benugo.com']
    start_urls = ['https://www.benugo.com/cafes/covent-garden/']

    def parse(self, response):
        menu_sections = response.xpath('//script[@type="application/ld+json"]/text()').getall()
        for menu_section in menu_sections[1:]:
            menu_section = json.loads(menu_section)
            menu_section_name = menu_section['name']
            sub_sections = menu_section['hasMenuSection']
            for sub_section in sub_sections:
                items = sub_section['hasMenuItem']
                sub_section_name = sub_section['name']
                for item in items:
                    yield {
                        'rest_name': 'Benugo Cafe',
                        'collection_date': date.today().strftime("%b-%d-%Y"),
                        'menu_section': menu_section_name + ',' + sub_section_name,
                        'item_name': item.get('name'),
                        'item_description': item.get('description'),
                        'carb': item.get('nutrition').get('carbohydrateContent'),
                        'kcal': item.get('nutrition').get('calories'),
                        'protein': item.get('nutrition').get('proteinContent'),
                        'satfat': item.get('nutrition').get('saturatedFatContent'),
                        'sugar': item.get('nutrition').get('sugarContent'),
                        'salt': item.get('nutrition').get('sodiumContent'),
                        'vegetarian': item.get('suitableForDiet')
                    }
