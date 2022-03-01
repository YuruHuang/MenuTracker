import json

import numpy as np
import pandas as pd
import requests
from bs4 import BeautifulSoup
from iteration_utilities import flatten

from define_collection_wave import folder
from helpers import create_folder, cleanhtml

path_mcdonalds = create_folder('1_McDonalds', folder)


def parse_json(dat):
    fileName = path_mcdonalds + '/item_' + str(item_id) + '.json'
    with open(fileName, 'w') as f:
        json.dump(dat, f)
    item_type = dat.get('item').get('item_type')
    nutrients = dat.get('item').get('nutrient_facts').get('nutrient')
    nutrient_dic = {}
    for i in range(len(nutrients)):
        nutrientName = nutrients[i]['nutrient_name_id']
        nutrientQuantity = nutrients[i]['value']
        nurteintHundred_g_per_product = nutrients[i]['hundred_g_per_product']
        nutrient_uom = nutrients[i]['uom']
        nutrient_adultDV = nutrients[i]['adult_dv']
        nutrient_childDV = nutrients[i]['child_dv']
        nutrient_dic.update({nutrientName + '_Quantity': nutrientQuantity,
                             nutrientName + '_100_g_per_product': nurteintHundred_g_per_product,
                             nutrientName + '_uom': nutrient_uom, nutrientName + '_adultDV': nutrient_adultDV,
                             nutrientName + '_childDV': nutrient_childDV})
    dat_dict = {
        'Product_Name': dat.get('item').get('item_name'),
        'Product_Title': dat.get('item').get('item_meta_title'),
        'Product_Description': dat.get('item').get('item_meta_description'),
        'Product_Ingredients': cleanhtml(dat.get('item').get('item_ingredient_statement')),
        'Product_Category': dat.get('item').get('default_category').get('category').get('name') if dat.get('item').get(
            'default_category') else 'NA',
        'item_type': item_type
    }
    dat_dict.update(nutrient_dic)
    return dat_dict

def parse_combo(dat):
    # combo meals --> get individual nutrient information and add them together
    fileName = path_mcdonalds + '/item_' + str(item_id) + '.json'
    with open(fileName, 'w') as f:
        json.dump(dat, f)
    item_type = dat.get('item').get('item_type')
    components = dat.get('item').get('components').get('component')
    components_list = []
    for component in components:
        component_id = component.get('id')
        url_component = f'https://www.mcdonalds.com/wws/json/getItemDetails.htm?country=UK&language=en&showLiveData=true&item={component_id}'
        dat_component = requests.get(url_component).json()
        parse_component = parse_json(dat_component)
        if float(parse_component.get('energy_kcal_100_g_per_product'))*100 !=0:
            parse_component.update({'servingweight': float(parse_component.get('energy_kcal_Quantity'))/float(parse_component.get('energy_kcal_100_g_per_product'))*100})
        else:
            parse_component.update({'servingweight': None})
        components_list.append(parse_component)
    # add the quantities (absolute energy) and % DV
    nutrients = {}
    for var in [key for key in components_list[0].keys() if 'Quantity' in key or 'DV' in key]:
        try:
            nutrients[var] = sum([float(component.get(var)) for component in components_list])
        except:
            nutrients[var] = None
    # weighted density
    for var in [key for key in components_list[0].keys() if '100_g_per_product'in key]:
        try:
            nutrients[var] = np.average([float(component.get(var)) for component in components_list], weights=[float(component.get('servingweight')) for component in components_list])
        except:
            pass
    # keep the same unit of measure
    for var in [key for key in components_list[0].keys() if 'uom'in key]:
        nutrients[var] = components_list[0].get(var)
    dat_dict = {
        'Product_Name': dat.get('item').get('item_name'),
        'Product_Title': dat.get('item').get('item_meta_title'),
        'Product_Description': ', '.join([component.get('Product_Name') for component in components_list]),
        'Product_Ingredients': cleanhtml(dat.get('item').get('item_ingredient_statement')),
        'Product_Category': dat.get('item').get('default_category').get('category').get('name') if dat.get('item').get(
            'default_category') else 'NA',
        'item_type': item_type
    }
    dat_dict.update(nutrients)
    return(dat_dict)



mcdonalds_url = 'https://www.mcdonalds.com/gb/en-gb/menu.html'
r = requests.get(mcdonalds_url)
soup = BeautifulSoup(r.text, 'html.parser')

# categories
categories = soup.find_all('a',{"class":"link key-arrow-move"})
category_links = ['https://www.mcdonalds.com' + category.get('href') for category in categories]
category_links = set(category_links)
item_ids = []
for category_link in category_links:
    #print(category_link)
    r = requests.get(category_link)
    soup = BeautifulSoup(r.text,'html.parser')
    items = soup.find_all('a', {"class": 'categories-item-link'}) #the new path
    # old path
    if len(items) == 0:
        items = soup.find_all('a', {"class": 'mcd-category-page__item-link'})
    ids = [item['data-at'].split(':')[3] for item in items[:-1]]
    #print(len(ids))
    item_ids.append(ids)

item_ids = list(flatten(item_ids))
item_ids = [item_id.replace('a','') for item_id in item_ids]
item_ids = set(item_ids)

mcdonalds_list = []
additional_items = []
for item_id in item_ids:
    url = f'https://www.mcdonalds.com/wws/json/getItemDetails.htm?country=UK&language=en&showLiveData=true&item={item_id}'
    dat = requests.get(url).json()
    if dat.get('item').get('relation_types'):
        related_items = dat.get('item').get('relation_types').get('relation_type')[0].get('related_items').get(
            'related_item')
        related_itemids = [related_item['id'] for related_item in related_items if related_item['id'] != int(item_id)]
        additional_items.extend(related_itemids)
    try:
        dict_temp = parse_json(dat)
    except:
        # likely a combo meal (e.g., happy meal with different components)
        dict_temp = parse_combo(dat)
    dict_temp.update({'item_id': item_id})
    mcdonalds_list.append(dict_temp)

for item_id in additional_items:
    url = f'https://www.mcdonalds.com/wws/json/getItemDetails.htm?country=UK&language=en&showLiveData=true&item={item_id}'
    dat = requests.get(url).json()
    dict_temp = parse_json(dat)
    dict_temp.update({'item_id': item_id})
    mcdonalds_list.append(dict_temp)

mcdonalds = pd.DataFrame(mcdonalds_list)
mcdonalds.to_csv(path_mcdonalds + '/mcdonalds_items.csv')