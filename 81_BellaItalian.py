from datetime import date

import pandas as pd
import requests
import scrapy

from define_collection_wave import folder
from helpers import create_folder

path_bella = create_folder('81_BellaItalian', folder)

items_all = []
url = 'https://menus.tenkites.com/thebigtg/mobilemenus03'
html = requests.get(url).text
page = scrapy.Selector(text=html)
menus = page.xpath('//div[@class="k10-menu-selector__option"]/span/@data-menu-identifier').getall()
menu_names = page.xpath('//div[@class="k10-menu-selector__option"]/span/span/text()').getall()
for i in range(len(menus)):
    menu_name = menu_names[i].strip()
    page = scrapy.Selector(text=requests.get(
        f'https://menus.tenkites.com//thebigtg/mobilemenus03?cl=true&mguid={menus[i]}&internalrequest=true').text)
    menu_sections = page.xpath('//section//section')
    for menu_section in menu_sections:
        menu_section_name = menu_section.xpath('normalize-space(.//div[@class="k10-course__name"]/text())').get()
        items = menu_section.xpath('.//div[@class="k10-l-grid__item"]')
        for item in items:
            # if substitution available
            item_vars = item.xpath('.//div[@class="k10-byo__item k10-byo-item k10-byo-item_recipe "]')
            item_description = item.xpath('normalize-space(.//div[@class="k10-byo-item__desc"]/text())').get()
            if len(item.xpath('.//div[@class="k10-byo__header"]')) > 0:
                wine_name = item.xpath(
                    'normalize-space(//div[@class="k10-byo__header"]//span[@class="k10-byo__name"]/text())').get()
                wine_description = item.xpath(
                    'normalize-space(//div[@class="k10-byo__header"]//div[@class="k10-byo__desc"]/text())').get()
                for item_var in item_vars:
                    item_name = wine_name + ' ' + item_var.xpath(
                        'normalize-space(.//span[@class="k10-byo-item__name"]/text())').get()
                    item_description = wine_description
                    item_dict = {
                        'rest_name': 'Bella Italia',
                        'collection_date': date.today().strftime("%b-%d-%Y"),
                        'item_name': item_name,
                        'item_description': item_description,
                        'menu_section': menu_name + ', ' + menu_section_name
                    }
                    nutrition_row = item_var.xpath('.//table//tr')
                    for row in nutrition_row:
                        item_dict.update({
                            row.xpath('./td[1]/text()').get():
                                row.xpath('./td[2]/text()').get()
                        })
                    items_all.append(item_dict)
            else:
                for item_var in item_vars:
                    item_name = item_var.xpath('normalize-space(.//span[@class="k10-byo-item__name"]/text())').get()
                    item_dict = {
                        'rest_name': 'Bella Italia',
                        'collection_date': date.today().strftime("%b-%d-%Y"),
                        'item_name': item_name,
                        'item_description': item_description,
                        'menu_section': menu_name + ', ' + menu_section_name
                    }
                    nutrition_row = item_var.xpath('.//table//tr')
                    for row in nutrition_row:
                        item_dict.update({
                            row.xpath('./td[1]/text()').get():
                                row.xpath('./td[2]/text()').get()
                        })
                    items_all.append(item_dict)

items_df = pd.DataFrame(items_all)
items_df.to_csv(path_bella + '/bella_items.csv')
