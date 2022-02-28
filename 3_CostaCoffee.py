import json
from define_collection_wave import folder
from helpers import create_folder,web_browser_path
from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import re
import pandas as pd

path_costa = create_folder('3_CostaCoffee', folder)

costa_url = "https://www.costa.co.uk/menu/"
options = webdriver.ChromeOptions()
# options.headless = True  # turn on the headless mode!
s=Service(web_browser_path)
browser = webdriver.Chrome(service=s)
browser.get(costa_url)
sleep(2)
# accept cookie
browser.find_element(by=By.ID, value='onetrust-accept-btn-handler').click()
sleep(3)
drink_buttons = browser.find_elements(by=By.CLASS_NAME, value= "productItem__Product-gctefu-0")

def parse_item(page, size=None, milk=None):
    soup = BeautifulSoup(page, 'html.parser')
    product_detail = soup.find_all('div', {'class': 'componentWrapperWhite'})
    product_name = product_detail[0].h1.text if product_detail[0].h1 else product_detail[0].h2.text
    product_description = product_detail[0].p.text if product_detail[0].p else "N/A"
    product_ingredients = soup.find('div', {'class': 'ingredients'}).text if soup.find('div', {
        'class': 'ingredients'}) else "N/A"
    alltables = soup.find_all('table')
    table_titles = [table.h2.text for table in alltables]
    # nutrition information collection
    nutrition_table = alltables[0]
    nutrition_columns = [name.text for name in nutrition_table.findAll('th')]
    nutrition_columns2 = [re.sub('\(.*?\)', '', name) for name in nutrition_columns]
    In_Store = [s for i, s in enumerate(nutrition_columns) if 'In-Store' in s]
    In_Store_column = In_Store[0] if In_Store else 'NA'
    Take_Out = [s for i, s in enumerate(nutrition_columns) if 'Take-Out' in s]
    Take_Out_column = Take_Out[0] if Take_Out else 'NA'
    serving_size_In_Store = In_Store_column[In_Store_column.find("(") + 1:In_Store_column.find(")")]
    serving_size_Take_Out = Take_Out_column[Take_Out_column.find("(") + 1:Take_Out_column.find(")")]
    row_dict = {'Product_Name': product_name, 'Product_Description': product_description,
                'Size': size, 'Milk': milk,
                'Product_Ingredients': product_ingredients}
    for row in nutrition_table.findAll('tr')[1:]:
        text = [item.text for item in row.findAll('td')]
        for i in range(len(text) - 1):
            row_dict.update({text[0] + '_' + nutrition_columns2[i + 1]: text[i + 1]})
    row_dict.update({'ServingSize_In_Store': serving_size_In_Store,
                     'ServingSize_Take_Out': serving_size_Take_Out})
    # allergen table
    allergen_table = alltables[3]
    for row in allergen_table.findAll('tr'):
        text = [item.text for item in row.findAll('td')]
        row_dict.update({text[0]: text[1]})
    # gluten table
    gluten_table = alltables[2]
    for row in gluten_table.findAll('tr'):
        text = [item.text for item in row.findAll('td')]
        row_dict.update({text[0]: text[1]})
    return row_dict


records = []
for drink in drink_buttons:
    category = drink.find_element_by_xpath(".//parent::div/preceding-sibling::div[@class='categoryHeader']").text
    drink.click()
    sleep(2)
    sizes = browser.find_elements(by=By.XPATH, value='//div[@class="filterGroup size"]/button')
    milk_choices = browser.find_elements(by=By.XPATH, value = '//div[@class="filterGroup milk"]/button')
    if len(sizes) > 0:
        for size in sizes:
            size.click()
            if len(milk_choices) > 0:
                for milk in range(len(milk_choices)):
                    milk_choices[milk].click()
                    row = parse_item(page=browser.page_source, milk=milk_choices[milk].text, size=size.text)
                    row.update({'Category': category})
                    records.append(row)
            else:
                row = parse_item(page=browser.page_source, size=size.text)
                row.update({'Category': category})
                records.append(row)
    else:
        if len(milk_choices) > 0:
            for milk in range(len(milk_choices)):
                milk_choices[milk].click()
                row = parse_item(page=browser.page_source, milk=milk_choices[milk].text)
                row.update({'Category': category})
                records.append(row)
        else:
            row = parse_item(page=browser.page_source)
            row.update({'Category': category})
            records.append(row)
    close_button = browser.find_element(by=By.XPATH, value = '//button[@class="closeButton"]')
    close_button.click()
    sleep(2)

browser.find_elements(by=By.XPATH, value = '//div[@class="pageSelect__StyledPageSelect-k46clq-0 dGJnrT"]/button')[1].click()
food_button = browser.find_elements(by=By.CLASS_NAME, value="productItem__Product-gctefu-0")

for food in range(len(food_button)):
    category = food_button[food].find_element_by_xpath(
        ".//parent::div/preceding-sibling::div[@class='categoryHeader']").text
    food_button[food].click()
    sleep(4)
    row = parse_item(page=browser.page_source)
    row.update({'Category': category})
    records.append(row)
    close_button = browser.find_element(by=By.XPATH, value = '//button[@class="closeButton"]')
    close_button.click()
    sleep(2)

browser.quit()
costa = pd.DataFrame(records)
# costa = costa.append(food_records)
costa.to_csv(path_costa + '/costa_items.csv')