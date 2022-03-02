import json

import requests

from define_collection_wave import folder
from helpers import create_folder, PDFDownloader

fg_path = create_folder('31_FlamingGrill', folder)
payload = {"operationName": "Menus", "variables": {"venueId": "6791"},
           "query": "query Menus($venueId: String!) {\n  menus(venueId: $venueId) {\n    id\n    name\n    slug\n    description\n    image\n  }\n}\n"}
headers_gk = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36',
    'origin': 'https://www.greeneking-pubs.co.uk',
    'referer': 'https://www.greeneking-pubs.co.uk/',
    'accept': '*/*',
    'content-type': 'application/json'
}
gk_url = 'https://menufinder.greeneking-pubs.co.uk/graphql'
menus = requests.post(gk_url, headers=headers_gk, data=json.dumps(payload)).json().get('data').get('menus')
for menu in menus:
    fg_urls = requests.post(gk_url, headers=headers_gk,
                            data=json.dumps({"operationName": "MenuPages",
                                             "variables": {"venueId": "6791", "menuId": menu.get('id')},
                                             "query": "query MenuPages($venueId: String!, $menuId: Int!) {\n  menuPages(venueId: $venueId, menuId: $menuId) {\n    id\n    name\n    downloads {\n      download\n      allergens\n      nutrition\n    }\n    keywords {\n      id\n      name\n      icon\n    }\n    displayGroups {\n      id\n      name\n      groupHeader\n      groupFooter\n      products {\n        id\n        name\n        description\n        new\n        showPrices\n        keywords\n        portions {\n          id\n          name\n          portionName\n          abbreviation\n          price\n        }\n      }\n    }\n  }\n}\n"}))
    urls_fordownload = fg_urls.json().get('data').get('menuPages').get('downloads').get('nutrition')
    if urls_fordownload is not None:
        filePath = fg_path + '/' + urls_fordownload.split('/')[-1]
        PDFDownloader('https://www.greeneking-pubs.co.uk' + urls_fordownload, filePath=filePath)
