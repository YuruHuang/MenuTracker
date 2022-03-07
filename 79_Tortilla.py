import json
from datetime import date

import pandas as pd
import requests

from define_collection_wave import folder
from helpers import create_folder

path_tortilla = create_folder('79_Tortilla', folder)
tortilla_url = 'https://www.tortilla.co.uk/wp-json/wp/v2/nutrition-api'
tortilla_json = requests.get(tortilla_url, verify=False).json()

with open(path_tortilla + '/tortilla.json', 'w') as f:
    json.dump(tortilla_json, f)

tortilla = []
for item in tortilla_json:
    item_id = item.get('id')
    item_name = item.get('title').get('rendered')
    steps = item.get('acf').get('nutrition_group')
    i = 0
    for step in steps:
        components = step.get('nutrition_product_subitem')
        i += 1
        for component in components:
            component.update({'collection_date': date.today().strftime("%b-%d-%Y"),
                              'rest_name': "Tortilla",
                              'menu_id': item_id,
                              'step': i,
                              'item_name': item_name
                              })
            tortilla.append(component)
tortilla_df = pd.DataFrame(tortilla)
tortilla_df.to_csv(path_tortilla + '/tortilla_items.csv')
