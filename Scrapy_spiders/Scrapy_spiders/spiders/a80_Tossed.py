import sys

import scrapy

sys.path.extend(['/Users/huangyuru/PycharmProjects/MenuTracker'])
from datetime import date
from selenium import webdriver
from helpers import web_browser_path
from time import sleep
from scrapy import Selector


class A80TossedSpider(scrapy.Spider):
    name = '80_Tossed'
    allowed_domains = ['api.amplitude.com', 'tosseduk.com', 'tosseduk.vmos.io']
    start_urls = [
        'https://tosseduk.vmos.io/store/34412cca-f374-497a-be27-f134e7693c34/menu/category/3d2af7ee-e21b-44b1-ad4c-0a6072d0fe2d/bundles?menuUUID=642a94ec-bea1-42a2-8ed1-79225c70aad6']

    def __init__(self):
        op = webdriver.ChromeOptions()
        op.add_argument('headless')
        self.driver = webdriver.Chrome(web_browser_path, options=op)

    def parse(self, response):
        self.driver.get(response.url)
        sleep(3)
        categories = self.driver.find_elements_by_xpath('//a[@data-test="store.menu.category.bundles"]')
        cat_names = self.driver.find_elements_by_xpath('//a[@data-test="store.menu.category.bundles"]/span')
        category_urls = [cat.get_attribute('href') for cat in categories]
        category_names = [cat.text for cat in cat_names]
        for i in range(len(category_urls)):
            self.driver.get(category_urls[i])
            cat_name = category_names[i]
            sleep(3)
            items = self.driver.find_elements_by_xpath('//div[@class="css-1fo9epc epmm7pg14"]')
            for i in range(len(items)):
                sleep(2)
                self.driver.find_elements_by_xpath('//div[@class="css-1fo9epc epmm7pg14"]')[i].click()
                sleep(3)
                try:
                    self.driver.find_element_by_xpath('//li[@data-test="tab-Nutrition"]').click()
                    sleep(2)
                    soup = Selector(text=self.driver.page_source)
                    nutrition = soup.xpath('//div[@data-test="tab-panel-nutrition"]//li')
                    nutrition_dict = {nutrient.xpath('./span[1]/text()').get():
                                          nutrient.xpath('./span[2]/text()').get() for nutrient in nutrition}
                    item_name = soup.xpath('//div[@class="css-13t6odn e1f6os763"]/h1/text()').get()
                    item_description = soup.xpath('//div[@class="css-1d2gjik e1f6os764"]/p/text()').get()
                    if item_name is None:
                        item_name = soup.xpath('//div[@class="css-1b960qj eii5z642"]//h1/text()').get()
                        item_description = soup.xpath('//div[@class="css-1e832z0 eii5z645"]/p/text()').get()
                    item_dict = {
                        'rest_name': 'Tossed',
                        'collection_date': date.today().strftime("%b-%d-%Y"),
                        'item_name': item_name,
                        'item_description': item_description,
                        'menu_section': cat_name
                    }
                    item_dict.update(nutrition_dict)
                    self.driver.find_element_by_xpath("//button[@data-test='customization-page-back-button']").click()
                    sleep(3)
                    yield item_dict
                except:
                    try:
                        self.driver.find_element_by_xpath(
                            "//button[@data-test='customization-page-back-button']").click()
                    except:
                        pass
