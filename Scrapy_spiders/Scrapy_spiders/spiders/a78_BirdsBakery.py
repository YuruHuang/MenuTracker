from datetime import date

import scrapy


class A78BirdsbakerySpider(scrapy.Spider):
    name = '78_BirdsBakery'
    allowed_domains = ['birdsbakery.com']
    start_urls = ['https://birdsbakery.com/allergens.html']

    def parse(self, response):
        categories = response.xpath('//li[@class="category"]')
        for category in categories:
            cat_name = category.xpath('.//h3/text()').get()
            items = category.xpath('.//div[@class="products"]/ul/li')
            for item in items:
                item_id = item.xpath('./@data-id').get()
                item_name = item.xpath('./div/text()').get()
                nutrition = response.xpath(f'//div[@class="allergen-{item_id} allergen"]')
                item_dict = {
                    'collection_date': date.today().strftime("%b-%d-%Y"),
                    'rest_name': "Birds Bakery",
                    'menu_section': cat_name,
                    'menu_id': item_id,
                    'item_name': item_name,
                    'allergens': nutrition.xpath('.//div[@class="allergen-info"]//div[@class="yes"]/text()').getall(),
                    'vegetarian': nutrition.xpath(
                        './/div[@class="intolerance-info"]//div[@class="yes"]/text()').getall()
                }
                rows = nutrition.xpath('.//div[@class="nutritionalInfo"]/div')
                for row in rows[1:]:
                    item_dict.update({row.xpath('./text()').get() + '_100': row.xpath('./span/text()').get()})
                yield item_dict
