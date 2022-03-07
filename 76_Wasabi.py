from datetime import date

import pandas as pd
import requests

from define_collection_wave import folder
from helpers import create_folder

path_wasabi = create_folder('76_Wasabi', folder)
wasabi_data = []
i = 1
menu_sections = requests.get('https://api.wasabi.uk.com/wp-json/wp/v2/category?per_page=100').json()
map_menu_cat = {str(cat.get('id')): cat.get('name') for cat in menu_sections}
loop = True
while loop == True:
    allitems = requests.get(f'https://api.wasabi.uk.com/wp-json/wp/v2/menuitem?page={i}&per_page=100').json()
    i += 1
    if len(allitems) != 100:
        loop = False
    for item in allitems:
        menu_section_id = item['category'][0]
        print(menu_section_id)
        item_dict = {
            'collection_date': date.today().strftime("%b-%d-%Y"),
            'rest_name': "Wasabi",
            'menu_section_id': menu_section_id,
            'menu_section': map_menu_cat[str(menu_section_id)],
            'item_name': item['yoast_title'].replace('-', ' '),
            'item_description': item['acf']['description'],
            'allergens': item['acf'].get('allergens')}
        if item['acf'].get('nutrition') is not None:
            item_dict.update({
                'kcal': item['acf']['nutrition']['energy']['value'],
                'protein_100': item['acf']['nutrition']['protein']['value'],
                'carb_100': item['acf']['nutrition']['carbohydrate']['value'],
                'fat_100': item['acf']['nutrition']['fat']['value'],
                'salt_100': item['acf']['nutrition']['salt']['value']})
        wasabi_data.append(item_dict)

wasabi_data_df = pd.DataFrame(wasabi_data)
wasabi_data_df.to_csv(path_wasabi + '/wasabi_items.csv')
