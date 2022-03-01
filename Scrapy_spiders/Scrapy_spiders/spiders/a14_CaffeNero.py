from time import sleep

import scrapy
from scrapy import Selector
from selenium import webdriver


class A14CaffeneroSpider(scrapy.Spider):
    name = '14_CaffeNero'
    allowed_domains = ['caffenero.com/uk']
    start_urls = ['https://caffenero.com/uk/coffee/']

    def __init__(self):
        self.driver = webdriver.Chrome("/chromedriver")

    def parse(self, response):
        # for url in response.url:
        self.driver.get(response.url)
        sleep(1)
        resp = Selector(text=self.driver.page_source)
        items = resp.xpath('//div[@class="product-inner"]/parent::div')
        for item in items:
            tables = item.xpath('.//table')
            for table in tables:
                label = table.xpath('./@class').get()
                if label != 'undefined undefined':
                    label = label.replace('undefined', '').strip()
                    item_name = item.xpath('.//div[@class="content"]/h3/text()').get() + ", " + label
                else:
                    item_name = item.xpath('.//div[@class="content"]/h3/text()').get()
                yield {
                    'collection_date': date.today().strftime("%b-%d-%Y"),
                    'rest_name': 'Caffe Nero',
                    'menu_section': response.url.split('/')[-2],
                    'item_name': item_name,
                    'item_description': item.xpath('.//div[@class="content"]/p/text()').get(),
                    'allergens': table.xpath('./following-sibling::ul[1]/li/text()').getall(),
                    'kj_100': table.xpath(".//td[contains(text(),'Energy')]/following-sibling::td[1]/text()").get(),
                    'kj': table.xpath(".//td[contains(text(),'Energy')]/following-sibling::td[2]/text()").get(),
                    'kcal_100':
                        table.xpath(".//td[contains(text(),'Energy')]/following-sibling::td[1]/text()").getall()[1],
                    'kcal': table.xpath(".//td[contains(text(),'Energy')]/following-sibling::td[2]/text()").getall()[1],
                    'fat_100': table.xpath(".//td[contains(text(),'Fat')]/following-sibling::td[1]/text()").get(),
                    'fat': table.xpath(".//td[contains(text(),'Fat')]/following-sibling::td[2]/text()").get(),
                    'satfat_100': table.xpath(
                        ".//em[contains(text(),'of which saturates')]/parent::td/following-sibling::td[1]/text()").get(),
                    'satfat': table.xpath(
                        ".//em[contains(text(),'of which saturates')]/parent::td/following-sibling::td[2]/text()").get(),
                    'carb_100': table.xpath(
                        ".//td[contains(text(),'Carbohydrates')]/following-sibling::td[1]/text()").get(),
                    'carb': table.xpath(
                        ".//td[contains(text(),'Carbohydrates')]/following-sibling::td[2]/text()").get(),
                    'sugar_100': table.xpath(
                        ".//em[contains(text(),'of which sugars')]/parent::td/following-sibling::td[1]/text()").get(),
                    'sugar': table.xpath(
                        ".//em[contains(text(),'of which sugars')]/parent::td/following-sibling::td[2]/text()").get(),
                    'fibre_100': table.xpath(
                        ".//td[contains(text(),'Fibre')]/following-sibling::td[1]/text()").get(),
                    'fibre': table.xpath(
                        ".//td[contains(text(),'Fibre')]/following-sibling::td[2]/text()").get(),
                    'protein_100': table.xpath(
                        ".//td[contains(text(),'Protein')]/following-sibling::td[1]/text()").get(),
                    'protein': table.xpath(
                        ".//td[contains(text(),'Protein')]/following-sibling::td[2]/text()").get(),
                    'salt_100': table.xpath(
                        ".//td[contains(text(),'Salt')]/following-sibling::td[1]/text()").get(),
                    'salt': table.xpath(
                        ".//td[contains(text(),'Salt')]/following-sibling::td[2]/text()").get(),
                    'sodium_100': table.xpath(
                        ".//td[contains(text(),'Sodium')]/following-sibling::td[1]/text()").get(),
                    'sodium': table.xpath(
                        ".//td[contains(text(),'Sodium')]/following-sibling::td[2]/text()").get()
                }
