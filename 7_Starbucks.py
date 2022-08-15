import requests
from helpers import create_folder,folder
import json
from datetime import date
from time import sleep
import pandas as pd

path_starbucks = create_folder('7_Starbucks', folder)

# unique menu items
categories = requests.get('https://www.starbucks.co.uk/api/v1/menu').json()
item_all = []
for cat in categories:
    menu_sections = cat.get('children')
    for menu_section in menu_sections:
        category_name = menu_section.get('elementId')
        item_groups = menu_section.get('children')
        if item_groups[0].get('children'):
            for item_group in item_groups:
                items = item_group.get('children')
        else:
            items = item_groups
        item_all.extend(items)


def parse_nutrition(page_json,item_name,menu_id, elementId, milk_value, size_value,url):
    item_dict = {
        'collection_date': date.today().strftime("%b-%d-%Y"),
        'rest_name': 'Starbucks',
        'item_name': item_name,
        'menu_id': menu_id,
        'element_id': elementId,
        'milk': milk_value,
        'size': size_value,
        'url': url
    }
    try:
        nutrition_dict = page_json.get('data').get('nutritions').get('nutritionals')
        for key in nutrition_dict.keys():
            item_dict.update({key:nutrition_dict.get(key).get('value')})
    except:
         pass
    return item_dict

# get different sizes
starbucks = []

for item in item_all[101:]:
    item_id = item.get('productNumber')
    item_name = item.get('name')
    print(item_name)
    url = item.get('href')
    elementId = item.get('elementId')
    page = requests.get(f'https://www.starbucks.co.uk/menu/product/info/{item_id}').json()
    try:
        selections = page.get('data').get('mainOptions').get('selectBoxes')
        fileName = path_starbucks + '/item_' + str(item_id) + '.json'
        with open(fileName, 'w') as f:
            json.dump(page, f)
        # endless number of combinations -> focus on milk and size
        if len(selections) == 1:
            if selections[0].get('title') == 'Size':
                size_options = selections[0].get('options')
        else:
            if selections.get('0').get('title') == 'Size':
                size_options = selections.get('0').get('options')
        for size in size_options:
            size_value = size.get('value')
            size_label = size.get('label')
            try:
                customisations_milk = page.get('data').get('customize').get('ingredientsGroups'). \
                    get('Milk & Dairy Alternatives').get('ingredients')
                milks = [c for c in customisations_milk if c.get('name') == 'milk-&-dairy-alternatives'][0].get('options')
                for milk in milks:
                    milk_label = milk.get('label')
                    page_milk_size = requests.post(f'https://www.starbucks.co.uk/menu/product/info/{item_id}',
                                                   json = {str(milk.get('value')):"1","productId":size_value}
                                                   ).json()
                    sleep(1)
                    row = parse_nutrition(page_milk_size,item_name,item_id, elementId, milk_label, size_label,url)
                    print(row)
                    print('------------------------------')
                    starbucks.append(row)
            except:
                page_size = requests.post(f'https://www.starbucks.co.uk/menu/product/info/{item_id}',
                                                   json = {"productId":item_id,"value":size_value,"name":"size"}
                                                   ).json()
                sleep(1)
                row = parse_nutrition(page_milk_size,item_name,item_id, elementId,  None, size_label,url)
                print(row)
                print('------------------------------')
                starbucks.append(row)
    except:
        # no size or milk choices
        row = parse_nutrition(page,item_name, item_id, elementId, None, None, url)
        print(row)
        print('------------------------------')
        starbucks.append(row)

starbucks_df = pd.DataFrame(starbucks)
starbucks_df.to_csv(path_starbucks + '/starbucks_items.csv')




