import re
from datetime import date

import scrapy


class A83TacobellSpider(scrapy.Spider):
    name = '83_TacoBell'
    allowed_domains = ['www.nutritionix.com']
    start_urls = ['https://www.nutritionix.com/taco-bell-uk/menu/premium']

    def parse(self, response):
        tablerows = response.xpath('//tbody/tr')
        for row in tablerows:
            if row.xpath('./@class').get() == 'subCategory':
                cat_name = row.xpath('.//h3/text()').get()
            else:
                id = row.xpath('.//a[@class="nmItem"]/@id').get().split('-')[-2]  # extract the id
                yield scrapy.Request(
                    url=f'https://www.nutritionix.com/taco-bell-uk/viewLabel/item/{id}/notFromAllergenPage',
                    callback=self.parse_item, meta={'id': id, 'category': cat_name})

    def parse_item(self, response):
        script = response.xpath('//script/text()').getall()[0]
        nutrition = [nutrition.replace('\nvalue', '') for nutrition in re.findall('\nvalue.*:.*,', script)]
        nutrient_dict = {}
        servingsize = re.search('valueServingWeightGrams : [0-9]+(.)?[0-9]?', script).group(0).split(' : ')[1]
        nutrient_dict.update({'ServingWeightGrams': servingsize})
        for nutrient in nutrition:
            header = nutrient.split(' : ')[0]
            value = nutrient.split(' : ')[1].replace(',', '')
            nutrient_dict.update({header: round(float(value))})
            nutrient_dict.update({header + '_100': round(float(value) / float(servingsize) * 100)})
        item_dict = {
            'collection_date': date.today().strftime("%b-%d-%Y"),
            'rest_name': 'Taco Bell',
            'item_id': response.meta['id'],
            'menu_section': response.request.meta['category'],
            'item_name': response.xpath('//div[@class="labelWrap fl"]/input[@id="valueName"]/@value').get(),
            'allergens': ', '.join(response.xpath('//td/strong/text()').getall()),
            'ingredients': response.xpath('//div/p')[1].xpath('string()').get(),
        }
        item_dict.update(nutrient_dict)
        yield item_dict
