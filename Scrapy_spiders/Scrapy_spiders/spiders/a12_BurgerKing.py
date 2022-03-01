# -*- coding: utf-8 -*-
from datetime import date
from time import sleep

import scrapy
from scrapy import Selector
from selenium import webdriver
from selenium.webdriver.common.by import By


def row_dance(rows):
    row_dict = {}
    for row in rows:
        nutrient = row.xpath('./span[1]/text()').get()
        nutrient_value = row.xpath('./span[2]/text()').get()
        row_dict.update({nutrient: nutrient_value})
    return row_dict


def update_nutrients(dict):
    new_dict = {}
    new_dict['kcal'] = re.sub("[^0-9^.]", "", dict['Energy'].split('/')[0].strip())
    new_dict['kj'] = re.sub("[^0-9^.]", "", dict['Energy'].split('/')[1].strip())
    new_dict['carb'] = re.sub("[^0-9^.]", "", dict['Carbohydrates'])
    new_dict['fat'] = re.sub("[^0-9^.]", "", dict['Fat'])
    new_dict['satfat'] = re.sub("[^0-9^.]", "", dict['Of which saturates'])
    new_dict['protein'] = re.sub("[^0-9^.]", "", dict['Proteins'])
    new_dict['salt'] = re.sub("[^0-9^.]", "", dict['Salt'])
    new_dict['sugar'] = re.sub("[^0-9^.]", "", dict['Of which sugars'])
    return new_dict


def prefix_100(dict):
    dict_new = {str(key) + '_100': val for key, val in dict.items()}
    return dict_new


class A12BurgerkingSpider(scrapy.Spider):
    name = '12_BurgerKing'
    allowed_domains = ['www.burgerking.co.uk']
    start_urls = ['https://www.burgerking.co.uk/nutrition-explorer']

    def __init__(self):
        self.driver = webdriver.Chrome('/Users/huangyuru/PycharmProjects/MenuStatUK/chromedriver')

    def parse(self, response):
        self.driver.get(response.url)
        sleep(10)
        # accept the cookie
        self.driver.find_element(by=By.XPATH, value='//button[@data-testid="accept-all-cookies-button"]').click()
        # expand all sections to display all menu items
        # expands = self.driver.find_elements_by_xpath(
        #     '//div[@class="dropdown-arrow__ArrowContainer-sc-143tfyi-0 gLiGSX"]')
        # for expand in expands[1:]:
        #     self.driver.execute_script("arguments[0].click();", expand)
        #     sleep(1)
        # menu sections
        # categories = WebDriverWait(self.driver, 20).until(EC.elements_to_be_clickable((By.XPATH, '//a[@class="tile-linkbk__TileLink-fepcm3-0 bMVAmV"]')))
        sleep(5)
        categories = self.driver.find_elements(by=By.XPATH, value='//section[contains(@class, "Container")]')
        for i in range(len(categories)):
            categories = self.driver.find_elements(by=By.XPATH, value='//section[contains(@class, "Container")]')
            category = categories[i]
            cat_name = category.find_element_by_xpath('.//h2').text
            category.click()
            sleep(5)
            items = category.find_elements(by=By.XPATH, value='.//div[contains(@class,"clickable-container")]')
            for item in items:
                sleep(2)
                item.click()
                sleep(2)
                resp = Selector(text=self.driver.page_source)
                item_element = resp.xpath('//div[@class="content-wrapper__ContentWrapper-fh0wv8-0 hlGrxd"]')
                if len(item_element) == 1:
                    if len(item_element.xpath('./h5[@data-testid="per-mass-header"]')) == 1:
                        rows_serving = item_element.xpath(
                            './h5[@data-testid="per-mass-header"]/preceding-sibling::div[contains(@class,"nutrient__Nutrient")]')
                        rows_density = item_element.xpath(
                            './h5[@data-testid="per-mass-header"]/following-sibling::div[contains(@class,"nutrient__Nutrient")]')
                        perserving = row_dance(rows_serving)
                        density = row_dance(rows_density)
                        perserving = update_nutrients(perserving)
                        density = prefix_100(update_nutrients(density))
                        perserving.update(density)
                    else:
                        rows_serving = item_element.xpath(
                            './h5[@data-testid="per-serving-header"]/following-sibling::div[contains(@class,"nutrient__Nutrient")]')
                        perserving = row_dance(rows_serving)
                        perserving = update_nutrients(perserving)
                    perserving.update({
                        'item_name': item_element.xpath(
                            './h3[@class="item-name__ItemName-sc-9r2cgr-0 jSpDpo"]/text()').get(),
                        'collection_date': date.today().strftime("%b-%d-%Y"),
                        'rest_name': 'Burger King',
                        'menu_section': cat_name
                    })
                yield perserving
                self.driver.find_element(by=By.XPATH,
                                         value='//button[@class="close-button__StyledButton-isthh2-0 eAURpv modal__StyledCloseButtonDefault-ihds1d-2 eGeNgW"]').click()
        self.driver.quit()
