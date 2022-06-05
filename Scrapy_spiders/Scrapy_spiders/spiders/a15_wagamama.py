from datetime import date
from time import sleep

import scrapy
from browserPath import web_browser_path
from scrapy import Selector
from selenium import webdriver
from selenium.webdriver.common.by import By


class A15WagamamaSpider(scrapy.Spider):
    name = '15_Wagamama'
    allowed_domains = ['www.wagamama.com']
    start_urls = ['https://www.wagamama.com/our-menu']

    def __init__(self):
        self.driver = webdriver.Chrome(web_browser_path)

    def parse(self, response):
        self.driver.get(response.url)
        sleep(20)
        # accept cookies
        # self.driver.find_element(by=By.XPATH, value='//button[@id="onetrust-accept-btn-handler"]').click()

        while len(self.driver.find_elements(by=By.XPATH, value='//li[@data-status="lazy"]')) > 0:
            toclick = self.driver.find_element(by=By.XPATH, value='//li[@data-status="lazy"]')
            self.driver.execute_script("arguments[0].click();", toclick)
            sleep(10)

        # categories = self.driver.find_elements_by_xpath('//ul[@class="k10-course-selector__wrapper-l1"]/li/span[@class="k10-course-selector__name"]')
        # for category in categories:
        #     cat_name = category.find_element_by_xpath('./span').text
        #     if cat_name is not None:
        #         category.click()

        resp = Selector(text=self.driver.page_source)
        self.driver.quit()
        products = resp.xpath('//div[@class="modal-content"]')
        for product in products:
            nutrient_dict = {}
            rows = product.xpath('.//tr[@class="k10-recipe-modal__tr"]')
            for row in rows[1:]:
                row_values = row.xpath('./td/text()').getall()
                nutrient = row_values[0]
                perserving = row_values[1]
                density = row_values[2]
                nutrient_dict.update({nutrient: perserving, nutrient + '_100': density})
            product_dict = {
                'rest_name': 'Wagamama',
                'collection_date': date.today().strftime("%b-%d-%Y"),
                'item_name': product.xpath('.//div[@class="k10-recipe-modal__name"]/text()').get(),
                'item_description': product.xpath('.//div[@class="k10-recipe-modal__desc"]/text()').get(),
                'allergens': product.xpath('normalize-space(.//div[@class="k10-recipe-modal__labels"]/text())').get()}
            product_dict.update(nutrient_dict)
            yield product_dict
