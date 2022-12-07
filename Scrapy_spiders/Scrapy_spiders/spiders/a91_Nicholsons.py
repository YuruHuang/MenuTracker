import scrapy
import re
from datetime import date

class A91NicholsonsSpider(scrapy.Spider):
    name = '91_Nicholsons'
    allowed_domains = ['www.smartchef.co.uk']
    start_urls = ['https://www.smartchef.co.uk/brands/nicholsons']

    def parse(self, response):
        menu_ids = response.xpath('.//div[@class="hidden-small"]/div/ul/li/a/@href').getall()
        for menu_id in menu_ids:
            menuid = re.findall("\'([^\"]*)\'", menu_id)[0]
            url = f'https://www.smartchef.co.uk/Brands/SuburbanMenuItems?menuid={menuid}'
            yield scrapy.Request(url=url, callback=self.parse_item)

    def parse_item(self, response):
        category = response.xpath('.//div[@class="visible-small"]/preceding-sibling::table//span/text()').get()
        items = response.xpath('.//div[@class="menuItem"]')
        for item in items:
            nutrients = item.xpath('.//span[@style="margin: 6px"]/text()').getall()
            if nutrients:
                kj = nutrients[0].split('/')[0]
                kcal = nutrients[0].split('/')[1]
                fat = nutrients[1]
                satfat = nutrients[2]
                carb = nutrients[3]
                sugar = nutrients[4]
                protein = nutrients[5]
                salt = nutrients[6]
            else:
                kj = None
                kcal = None
                fat = None
                satfat = None
                carb = None
                sugar = None
                protein = None
                salt = None
            yield {
                'collection_date': date.today().strftime("%b-%d-%Y"),
                'rest_name': 'Nicholson\'s',
                'menu_section': category,
                'item_name': item.xpath('./p/span[1]/text()').get(),
                'item_description': item.xpath('./p/span[2]/text()').get(),
                'allergens': item.xpath('./p/span[3]/text()').get(),
                'kj': kj,
                'kcal': kcal,
                'fat': fat,
                'satfat': satfat,
                'carb': carb,
                'sugar': sugar,
                'protein': protein,
                'salt': salt
            }