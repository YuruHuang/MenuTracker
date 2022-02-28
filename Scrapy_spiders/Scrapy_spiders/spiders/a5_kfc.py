import scrapy
from time import sleep
from scrapy import Selector
import json
from datetime import date
from selenium import webdriver


class A5KfcSpider(scrapy.Spider):
    name = '5_KFC'
    allowed_domains = ['www.kfc.co.uk/nutrition-allergens']
    start_urls = ['https://www.kfc.co.uk/nutrition-allergens']

    def __init__(self):
        self.driver = webdriver.Chrome('/Users/huangyuru/PycharmProjects/MenuStatUK/chromedriver')

    def parse(self, response):
        self.driver.get(response.url)
        sleep(2)
        page_source = Selector(text = self.driver.page_source)
        self.driver.quit()
        dat = json.loads(page_source.xpath('//script[@id="__NEXT_DATA__"]/text()').get())
        items = dat.get('props').get('pageProps').get('data').get('mainContent')[2].get('data').get("children").get("products")
        for item in items:
            allergens = item.get('allergens')
            allergen_list = [allergen for allergen in allergens.keys() if allergens.get(allergen).get('type') is not False]
            # this list includes primary and secondary allergens (not sure what it means)
            nutrients = item.get('nutrition')
            vegan = item.get('vegan')
            vegetarian = item.get('vegetarian')
            item_dict =  {
                'rest_name': 'KFC',
                'collection_date': date.today().strftime("%b-%d-%Y"),
                'item_name': item.get('name'),
                'menu_section': item.get('categories')[0],
                'allergens': allergen_list,
                'vegan': vegan,
                'vegetarian': vegetarian
            }
            item_dict.update(nutrients)
            yield item_dict
