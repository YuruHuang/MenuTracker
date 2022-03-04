import json
from datetime import date

import pandas as pd
import requests

from define_collection_wave import headers, folder
from helpers import create_folder

path_pure = create_folder('64_Pure', folder)

# REWROTE THE CODE - nutritional info through the API
pure_requesturl = 'https://pure-uk.5loyalty.com/nutrition_data'
pure_nutrition = requests.get(pure_requesturl, headers=headers).json()
path_nutrition = path_pure + '/pure_nutrition.json'
with open(path_nutrition, 'w') as f:
    json.dump(pure_nutrition, f)
pure_menuurl = 'https://pure-uk.5loyalty.com/get_default_menu/5L%20Main%20Menu%20-%20JUNE'  # default menu
pure_menu = requests.get(pure_menuurl, headers=headers).json()
path_menu = path_pure + '/pure_menu.json'
with open(path_menu, 'w') as f:
    json.dump(pure_menu, f)

pure_list = []
groups = pure_menu.get('data').get('menuEntryGroups')
for group in groups:
    cat_name = group.get('name')
    items = group.get('menuEntry')
    for item in items:
        item_dict = {
            'rest_name': 'Pure.',
            'collection_date': date.today().strftime("%b-%d-%Y"),
            'menu_section': cat_name,
            'menu_id': item.get('sku'),
            'item_name': item.get('productName'),
            'item_description': item.get('description'),
            'price': item.get('productPrice'),
            'allergens': item.get('itemRichData').get('allergenCodes')
        }
        pure_list.append(item_dict)

pure_menu = pd.DataFrame(pure_list)

pure_nutritionlist = []
nutrition = pure_nutrition.get('data')
for nut in nutrition:
    nutrition_dict = {
        'menu_id': nut.get('sku'),
        'ingredients': nut.get('ingredients'),
    }
    nutrients = nut.get('items')
    for nutrient in nutrients:
        nutrition_dict.update({
            nutrient.get('item') + 'perserving': nutrient.get('amountPerServing'),
            nutrient.get('item') + 'per100': nutrient.get('amountPer100')
        })
    pure_nutritionlist.append(nutrition_dict)

pure_nutrition = pd.DataFrame(pure_nutritionlist)

pure_all = pd.merge(pure_menu, pure_nutrition, on='menu_id', how='left')
pure_all.to_csv(path_pure + '/pure_items.csv')
