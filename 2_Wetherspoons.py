import requests
from helpers import create_folder
import json
from define_collection_wave import folder
import pandas as pd

path_wetherspoons = create_folder('2_Wetherspoons',folder)

def wetherspoonsCrawler(pub_id):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36',
        'APIKey': 'YVB5QfeRKUK1+EGvXGjPgQA93reRTUJHsCuQSHR+=='}
    url = f'https://www.jdwetherspoon.com//api/v2/pubs/{pub_id}/food'
    resp = requests.get(url, headers=headers)
    items = resp.json()
    fileName = path_wetherspoons + '/pub_' + str(pub_id) + '.json'
    with open(fileName, 'w') as f:
        json.dump(items, f)
    return pd.DataFrame(items)

wetherspoon = wetherspoonsCrawler(pub_id=70)
wetherspoon.to_csv(path_wetherspoons + '/Wetherspoons_items.csv')
