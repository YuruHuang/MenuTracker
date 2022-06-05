import json
from datetime import date

import scrapy


def get_nutrient(nutrient_name, item):
    try:
        return item.get('nutrition').get(nutrient_name)
    except:
        return None


class A41BenugoSpider(scrapy.Spider):
    name = '42_Benugo'
    allowed_domains = ['www.benugo.com']
    start_urls = ['https://www.benugo.com/cafes/clerkenwell/']

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
                        'carb': get_nutrient('carbohydrateContent', item),
                        'kcal': get_nutrient('calories', item),
                        'protein': get_nutrient('proteinContent', item),
                        'satfat': get_nutrient('saturatedFatContent', item),
                        'sugar': get_nutrient('sugarContent', item),
                        'salt': get_nutrient('sodiumContent', item),
                        'vegetarian': item.get('suitableForDiet')
                    }
