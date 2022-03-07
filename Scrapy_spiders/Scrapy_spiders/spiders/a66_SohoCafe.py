from datetime import date

import scrapy


class A66SohocafeSpider(scrapy.Spider):
    name = '66_SohoCafe'
    allowed_domains = ['sohocoffee.com']
    start_urls = ['https://sohocoffee.com/menus/']

    def parse(self, response):
        categories = response.xpath('//div[@class="tab-content"]/div')
        for category in categories:
            cat_name = category.xpath('./@data-id').get()
            items = category.xpath('.//div[@class="modal"]')
            for item in items:
                energy = item.xpath('.//table[@class="energy-table"]')
                headers = energy.xpath('.//td/strong/text()').getall()
                values = energy.xpath('.//td/text()').getall()
                energy_dict = dict(zip(headers, values))
                nutrition = item.xpath('.//table[@class="nutritional-table"]')
                headers = nutrition.xpath('./thead/tr/td/text()').getall()
                rows = nutrition.xpath('./tbody/tr')
                nutrient_dict = {}
                for row in rows:
                    nutrient = row.xpath('./td[1]/text()').get()
                    for i in range(2, (len(headers) + 2)):
                        value = row.xpath(f'./td[{i}]/text()').get().replace(',', '')
                        key = nutrient + '_' + headers[i - 2]
                        nutrient_dict.update({key: value})
                item_dict = {
                    'collection_date': date.today().strftime("%b-%d-%Y"),
                    'rest_name': 'Soho Coffee',
                    'menu_section': cat_name,
                    'item_name': item.xpath('.//div[@class="bit-80"]/h2/text()').get(),
                    'item_description': item.xpath('normalize-space(.//div[@class="bit-80"]/p/text())').get(),
                    'allergens': ' ,'.join(
                        [allergen.strip() for allergen in item.xpath('.//div[@class="bit-2"]/h5/text()').getall()]),
                }
                item_dict.update(energy_dict)
                item_dict.update(nutrient_dict)
                yield item_dict
