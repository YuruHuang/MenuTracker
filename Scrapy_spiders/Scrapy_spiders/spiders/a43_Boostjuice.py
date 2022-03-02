from datetime import date

import scrapy


class A43BoostjuiceSpider(scrapy.Spider):
    name = '43_Boostjuice'
    allowed_domains = ['www.boostjuicebars.co.uk']
    start_urls = ['https://www.boostjuicebars.co.uk/drinks/']

    def parse(self, response):
        drinks = response.xpath('//ul[@id="og-grid"]/li/a/@id').getall()
        for drink in drinks:
            print(drink)
            yield scrapy.Request(url='https://www.boostjuicebars.co.uk/drinks/' + drink, callback=self.parse_item)

    def parse_item(self, response):
        item_name = response.xpath('//div[@class="quick-overview"]/h2/text()').get()
        item_desc = response.xpath('//div[@class="quick-overview"]/p/text()').get()
        servingsizes = response.xpath('//div[@class="tabs-nav"]/a/text()').getall()
        org = response.xpath('//div[@class="org info-table"]/ul/li/strong/text()').getall()
        med = response.xpath('//div[@class="med info-table"]/ul/li/strong/text()').getall()
        kids = response.xpath('//div[@class="kid info-table"]/ul/li/strong/text()').getall()
        nutrient_list = [org]
        if len(med) > 0:
            nutrient_list.append(org)
        if len(kids) > 0:
            nutrient_list.append(kids)
        headers = ['kj', 'fat', 'carb', 'fibre', 'protein', 'satfat', 'sugar', 'sodium']
        item_dict = {
            'rest_name': 'Boost Juice Bars',
            'collection_date': date.today().strftime("%b-%d-%Y"),
            'item_name': item_name,
            'item_description': item_desc
        }
        for i in range(len(servingsizes)):
            if len(servingsizes) == 1:
                nutrition_dict = dict(zip(headers, org))
            else:
                nutrition_dict = dict(zip(headers, nutrient_list[i]))
            nutrition_dict.update({'servingsize': servingsizes[i]})
            item_dict.update(nutrition_dict)
            yield item_dict
