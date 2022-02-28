from define_collection_wave import folder
from helpers import create_folder, headers
import requests
from datetime import date
import json
import pandas as pd

path_greggs = create_folder('4_Greggs',folder)

request_url = 'https://production-digital.greggs.co.uk/api/v1.0/articles/masters?ExcludeUnpublished=true&ExcludeDuplicates=true&ExcludeHiddenFromMenu=true'
product_list = requests.get(request_url, headers=headers).json()
with open(path_greggs + '/greggs.json', 'w') as f:
    json.dump(product_list, f)

greggs = []
category_map = requests.get('https://api.storyblok.com/v2/cdn/datasource_entries/?datasource=category-ids&version=published&token=KLOrdhTNVjQnjwj0IppdrAtt').json().get('datasource_entries')
lookup = {cat.get('value'): cat.get('name')for cat in category_map}
for product in product_list:
    cat_id = product.get('articleCategoryId')
    product_dict = {
        'collection_date':date.today().strftime("%b-%d-%Y"),
        'rest_name': 'Greggs',
        'menu_id': product.get('articleCode'),
        'item_name': product.get('articleName'),
        'servingsize': product.get('articleSize').get('size'),
        'servingsizeunit': product.get('articleSize').get('unitOfMeasure'),
        'item_description': product.get('customerDescription').strip(),
        'category': lookup[str(cat_id)],
        'allergens': [allergen.get('name') for allergen in product.get('ingredients')]}
    nutrient_dict = product.get('nutritionalValues')
    for nutrient in nutrient_dict:
        product_dict.update({nutrient.get('name'):nutrient.get('value'),
                             nutrient.get('name')+'_100': nutrient.get('valuePerHundredArticleSizeUnit')})
    greggs.append(product_dict)
greggs = pd.DataFrame(greggs)
greggs.to_csv(path_greggs + '/greggs_items.csv')