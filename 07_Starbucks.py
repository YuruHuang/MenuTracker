import requests

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

# get different sizes
additional_sizes = []
i = 1
for item in item_all:
    print(i)
    i += 1
    item_id = item.get('productNumber')
    page = requests.get(f'https://www.starbucks.co.uk/menu/product/info/{item_id}').json()
    selections = page.get('data').get('mainOptions').get('selectBoxes')
    if len(selections) == 1:
        if selections[0].get('title') == 'Size':
            size_options = selections[0].get('options')
    else:
        if selections.get('0').get('title') == 'Size':
            size_options = selections.get('0').get('options')
    for size in size_options:
        additional_sizes.append(size.get('value'))
