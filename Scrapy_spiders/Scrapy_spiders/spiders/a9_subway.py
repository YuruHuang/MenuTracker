from datetime import date

import requests
import scrapy


class A9SubwaySpider(scrapy.Spider):
    name = '9_Subway'
    allowed_domains = ['www.subway.com']
    start_urls = ['https://www.subway.com/en-gb/menunutrition']

    def parse(self, response):
        categories = response.xpath('//a[@class="menu-panel-class-main"]/@href').getall()
        for category in categories:
            cat_name = category.split('/')[-1]
            yield scrapy.Request(
                url='https://www.subway.com' + category, callback=self.parse_category,
                meta={'cat_name': cat_name}
            )

    def parse_category(self, response):
        items = response.xpath('//div[@class="menu-category-type clearfix"]/div')
        for item in items:
            if item.xpath('./@id').get() is not None:
                productID = item.xpath('./@id').get().split('_')[1]
                yield scrapy.Request(url='https://www.subway.com' + item.xpath('./a/@href').get(),
                                     callback=self.parse_item, meta={'productID': productID,
                                                                     'cat_name': response.meta['cat_name']})

    def parse_item(self, response):
        productID = response.meta['productID']
        item_dict = {
            'collection_date': date.today().strftime("%b-%d-%Y"),
            'rest_name': "Subway",
            'menu_section': response.meta['cat_name'],
            'menu_id': productID,
            'item_name': response.xpath('//span[@id="main_0_centercolumn_0_lblPdtTitle"]/text()').get(),
            'item_description': response.xpath(
                'normalize-space(//span[@id="main_0_centercolumn_0_lblDesc"]/text())').get(),
        }
        type = response.xpath('//input[@id="main_0_centercolumn_0_lblHiddenMenuBuildProductTypeID"]/@value').get()
        nutrition = requests.get(f'https://www.subway.com/UserControls/Menu/Controls/NutritionCalculatorHandler.'
                                 f'ashx?Calculate=1&productId={productID}&productBuildTypeId={type}&countryCode='
                                 f'UKM&languageCode=ENG&serving=serving').json()[1]
        for nutrient in nutrition:
            item_dict.update({nutrient['DisplayName']: nutrient['Value']})
        yield item_dict
