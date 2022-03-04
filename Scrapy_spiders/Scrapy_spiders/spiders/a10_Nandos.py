from time import sleep

import scrapy
from scrapy import Selector
from selenium import webdriver


class A10NandoSpider(scrapy.Spider):
    name = '10_Nandos'
    allowed_domains = ['nandos.co.uk']
    start_urls = ['https://nandos.co.uk/food/menu/index.html']

    def __init__(self):
        self.driver = webdriver.Chrome("/Users/huangyuru/PycharmProjects/MenuStatUK/chromedriver")

    def parse(self, response):
        self.driver.get(response.url)
        sleep(1)
        # accept the cookies
        self.driver.find_element_by_xpath('//button[@id="truste-consent-button"]').click()
        sleep(0.5)

        items = self.driver.find_elements_by_xpath('//div/button[contains(@title, "Open product description for")]')
        for item in items:
            category = item.find_element_by_xpath('./parent::div/preceding-sibling::h2/em').text
            self.driver.execute_script("arguments[0].click();", item)
            sleep(1)
            item_button = self.driver.find_element_by_xpath(
                '//ul[@class="tablist"]/li[text()="Nutritional information"]')
            self.driver.execute_script("arguments[0].click();", item_button)
            sleep(1)
            resp = Selector(text=self.driver.page_source)
            close_button = self.driver.find_element_by_xpath('//a[@class="close"]')
            self.driver.execute_script("arguments[0].click();", close_button)
            sleep(1)
            # assuming all products have the same nutrients
            yield {
                'Product Name': resp.xpath('//div[@class="inner"]/h3/text()').get(),
                'Product Description': resp.xpath('//div[@class="inner"]/p/text()').get(),
                'Product Price': resp.xpath('//div[@class="inner"]/div[@class="price"]/text()').get(),
                'Product Category': category,
                'Energy (kcal) per serving': resp.xpath('//div[@class="block n"]/table/tbody/tr[1]/th[2]/text()').get(),
                'Energy (kj) per serving': resp.xpath('//div[@class="block n"]/table/tbody/tr[2]/td[2]/text()').get(),
                'Fat per serving': resp.xpath('//div[@class="block n"]/table/tbody/tr[3]/th[2]/text()').get(),
                'Saturated fat per serving': resp.xpath('//div[@class="block n"]/table/tbody/tr[4]/td[2]/text()').get(),
                'Carbohydrates per serving': resp.xpath('//div[@class="block n"]/table/tbody/tr[5]/th[2]/text()').get(),
                'Sugar per serving': resp.xpath('//div[@class="block n"]/table/tbody/tr[6]/td[2]/text()').get(),
                'Fibre per serving': resp.xpath('//div[@class="block n"]/table/tbody/tr[7]/th[2]/text()').get(),
                'Protein per serving': resp.xpath('//div[@class="block n"]/table/tbody/tr[8]/th[2]/text()').get(),
                'Salt per serving': resp.xpath('//div[@class="block n"]/table/tbody/tr[9]/th[2]/text()').get()
            }
        self.driver.quit()
