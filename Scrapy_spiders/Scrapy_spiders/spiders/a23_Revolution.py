from datetime import date
from time import sleep

import scrapy
from scrapy import Selector
from selenium import webdriver


class A23RevolutionSpider(scrapy.Spider):
    name = '23_Revolution'
    allowed_domains = ['www.revolution-bars.co.uk']
    # start_urls = ['https://www.revolution-bars.co.uk/bar/london-america-square/menus/food-menu/']
    start_urls = ['https://www.revolution-bars.co.uk/bar/london-clapham-high-street/menus/food-menu/']

    def __init__(self):
        self.driver = webdriver.Chrome("/Users/huangyuru/PycharmProjects/MenuStatUK/chromedriver")

    def parse(self, response):
        self.driver.get(response.url)
        sleep(10)
        items = self.driver.find_elements_by_xpath('//div[@class="menusitem"]')
        resp_new = Selector(text=self.driver.page_source)
        itemnames = resp_new.xpath(f'//div[@class="menusitem"]//p/strong/text()').getall()
        for i in range(len(items)):
            item = self.driver.find_elements_by_xpath('//li[@id="nutritional-info"]')[i]
            self.driver.execute_script("arguments[0].scrollIntoView();", item)
            self.driver.execute_script("arguments[0].click();", item)
            sleep(1)
            resp = Selector(text=self.driver.page_source)
            nutrients = resp.xpath('.//div[@class="menusitem__nutrition-value"]/text()').getall()
            kcal = nutrients[0] if len(nutrients) > 2 else None
            fat = nutrients[1] if len(nutrients) > 2 else None
            satfat = nutrients[2] if len(nutrients) > 2 else None
            carb = nutrients[3] if len(nutrients) > 2 else None
            protein = nutrients[4] if len(nutrients) > 2 else None
            sodium = nutrients[5] if len(nutrients) > 2 else None
            item_name = itemnames[i]
            item_desc = resp.xpath(f'(//div[@class="menusitem"])[{i + 1}]//div[@class="desc"]/text()').get()
            price = resp.xpath(f'(//div[@class="menusitem"])[{i + 1}]//p[@class="price"]/text()').get()
            allergens = resp.xpath(
                f'string((//div[@class="menusitem"])[{i + 1}]//div[@class="font--mediumgrey font--small font--italic pt-1"])').get()
            yield {
                'collection_date': date.today().strftime("%b-%d-%Y"),
                'rest_name': 'Revolution Vodka Bars',
                'menu_section': response.url.split('/')[-2],
                'item_name': item_name,
                'item_description': item_desc,
                'price': price,
                'allergens': allergens,
                'kcal': kcal,
                'fat': fat,
                'satfat': satfat,
                'carb': carb,
                'protein': protein,
                'sodium': sodium
            }
