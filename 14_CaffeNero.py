from datetime import date

import pandas as pd
import requests

from define_collection_wave import folder
from helpers import create_folder

caffenero_path = create_folder('14_CaffeNero', folder)

# find start URLs
url_request = 'https://caffenero-webassets-production.s3.eu-west-2.amazonaws.com/menus/menu_gb_en-gb.json'
headers = {
    'x-amz-id-2': 'PhizYabIyH2XeoTq5usCM6p/191DEQZuI5ieZQr2aI41vHGyggWLaxw82DIA1pYYuPBFV7GU2o4=',
    'x-amz-request-id': '4V82CASKYFW224S1'
}

response_nero = requests.get(url_request, headers=headers).json()


def parse_nutrition(json_nutrition):
    nutrient_dict = {}
    for nutrient in json_nutrition:
        nutrient_dict.update({
            nutrient + '_100': json_nutrition.get(nutrient).get('per_100g'),
            nutrient: json_nutrition.get(nutrient).get('per_product'),
            nutrient + '_uom': json_nutrition.get(nutrient).get('units')
        })
    return nutrient_dict


def parse_page(variant, item_name_new, item_description, section_name):
    dietary = variant.get('dietary')
    nutrition = parse_nutrition(variant.get('nutrition'))
    product_dict = {
        'collection_date': date.today().strftime("%b-%d-%Y"),
        'rest_name': 'Caffe Nero',
        'item_name': item_name_new,
        'item_description': item_description,
        'dietary': dietary,
        'menu_section': cat_name + ', ' + section_name
    }
    product_dict.update(nutrition)
    list.append(product_dict)


def parse_item(json_products, list):
    if json_products.get('menus') == []:
        sections = json_products.get('sections')
        for section in sections:
            section_name = section.get('details').get('title')
            products = section.get('products')
            for product in products:
                item_name = product.get('details').get('title')
                item_description = product.get('details').get('description').strip()
                variants = product.get('variants')
                for variant in variants.keys():
                    variant_ = variants.get(variant)
                    if variant != 'default':
                        item_name_new = item_name + ', ' + variant
                    else:
                        item_name_new = item_name
                    for variant__ in variant_.keys():
                        if variant__ != 'default':
                            item_name_new_new = item_name_new + ', ' + variant__
                        else:
                            item_name_new_new = item_name_new
                        parse_page(variant_.get(variant__), item_name_new_new, item_description, section_name)
    else:
        for menu in json_products.get('menus'):
            parse_item(menu, list)


list = []
for category in response_nero:
    cat_name = category.get('details').get('title')
    parse_item(category, list)

caffenero_df = pd.DataFrame(list)
caffenero_df.to_csv(caffenero_path + '/caffenero_items.csv')
