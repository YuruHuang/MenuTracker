from datetime import date
from time import sleep

import scrapy
from browserPath import web_browser_path
from scrapy import Selector
from selenium import webdriver
from selenium.webdriver.common.by import By



class A55JoejuiceSpider(scrapy.Spider):
    name = '55_JoeJuice'
    allowed_domains = ['orders.joejuice.com']
    store_id = '186f925b-8932-4195-8e67-6e5d01b8bfc2'
    start_urls = [f'https://orders.joejuice.com/store/{store_id}']

    # an alternative way to do this is through the API request (request to get ingredients and their portions,
    # and then query their nutritional, allergen, and price information. But I cannot seem to find this information
    # on websites

    def __init__(self):
        self.driver = webdriver.Chrome(web_browser_path)

    def parse(self, response):
        self.driver.get(response.url)
        sleep(10)
        self.driver.find_element_by_id('declineButton').click()
        sleep(1)
        categories = self.driver.find_elements(by = By.XPATH, value = '//div[@data-cy="product-subheader"]')
        for i in range(len(categories)):
            cat_name = categories[i].text
            items = categories[i].find_elements(by = By.XPATH, value='./following-sibling::div/div[contains(@class,"item")]')
            for j in range(len(items)):
                item = self.driver.find_element(by=By.XPATH, value=f'((//div[@data-cy="product-subheader"])[{i + 1}]/following-sibling::div/div[contains(@class,"item")])[{j + 1}]')
                item_description = item.find_element_by_xpath('.//p[@class="MuiTypography-root jss98 MuiTypography-caption MuiTypography-colorTextPrimary"]').text
                item_price = item.find_element_by_xpath('.//p[@class="MuiTypography-root MuiTypography-caption MuiTypography-colorTextPrimary MuiTypography-alignLeft"]').text
                item_button = self.driver.find_element_by_xpath(f'((//div[@data-cy="product-subheader"])[{i + 1}]/following-sibling::div/div[contains(@class,"item")])[{j + 1}]//button')
                self.driver.execute_script("arguments[0].click();", item_button)
                sleep(3)
                try:
                    button = self.driver.find_element_by_xpath('//button[@class="MuiButtonBase-root MuiButton-root MuiButton-text jss14 MuiButton-textPrimary"]')
                    self.driver.execute_script("arguments[0].click();", button)
                    sleep(5)
                    item_page = Selector(text=self.driver.page_source)
                    sleep(5)
                    back_button = self.driver.find_element_by_xpath('//button[@data-cy="modal-sticky-header-button"]')
                    self.driver.execute_script("arguments[0].click();", back_button)
                    sleep(3)
                except:
                    print('no nutritional information available ')
                    item_page = Selector(text=self.driver.page_source)
                try:
                    self.driver.find_element_by_xpath('//button[@data-cy="modal-sticky-header-button"]').click()
                    sleep(2)
                except:
                    pass
                allergens = item_page.xpath('//h3[contains(text(),"Allergens")]/parent::div/ul/li')
                nutrients = item_page.xpath('//h3[contains(text(),"Nutrition")]/parent::div/ul/li')
                item_dict = {
                    'collection_date': date.today().strftime("%b-%d-%Y"),
                    'rest_name': 'JOE & THE JUICE',
                    'menu_section': cat_name,
                    'item_name': item_page.xpath('//h3[@data-cy="product-title"]/text()').get(),
                    'item_description': item_description,
                    'price': item_price
                }
                if allergens == []:
                    yield item_dict
                else:
                    allergens_list = []
                    for allergen in allergens:
                        allergens_list.append(allergen.xpath('(./div)[2]/text()').get() + ' ' + allergen.xpath(
                            '(./div)[1]/span/text()').get())
                    item_dict.update({'allergens': allergens_list})
                    for nutrient in nutrients:
                        item_dict.update(
                            {nutrient.xpath('(./div)[1]/span/text()').get(): nutrient.xpath('(./div)[2]/text()').get()})
                    yield item_dict
        self.driver.quit()
