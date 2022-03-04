from datetime import date

import pandas as pd
import requests

from define_collection_wave import folder
from helpers import headers, create_folder

# collect the menu for the London Peckham location at 12pm
path_morrisons = create_folder('61_MorrisonsCafe', folder)
location = '306EI'
time_slot = '12:00'

url_category = f'https://www.morrisons.com/cafe/menudata/{location}/Category/0?timeSlot={time_slot}&firstCall=true'
categories = requests.get(url_category, headers=headers).json()

items = []
for category in categories.get('categories'):
    cat_id = category.get('categoryId')
    cat_url = f'https://www.morrisons.com/cafe/menudata/306EI/Category/{cat_id}?timeSlot={time_slot}'
    cat_data = requests.get(cat_url, headers=headers).json()
    cat_name = cat_data.get('categoryTitle')
    menu_items = cat_data.get('menuItems')
    for menu_item in menu_items:
        item_dict = {
            'collection_date': date.today().strftime("%b-%d-%Y"),
            'rest_name': 'Morrisons Cafe',
            'menu_section': cat_name,
            'item_name': menu_item.get('menuItemName'),
            'item_id': menu_item.get('menuItemId'),
            'price': menu_item.get('menuItemBasePrice'),
            'kcal': menu_item.get('kcal')
        }
        items.append(item_dict)

items_df = pd.DataFrame(items)
items_df.to_csv(path_morrisons + '/' + 'MorrisonsCafe_items.csv')
