from datetime import date

import scrapy


class A38ItsuSpider(scrapy.Spider):
    name = '38_Itsu'
    allowed_domains = ['www.itsu.com']
    start_urls = ['https://www.itsu.com/menu']

    def parse(self, response):
        items = response.xpath('//div[@class="item col-md-4 col-6"]/a/@href').getall()
        # menu_section = response.request.url.split('/')[-2]
        for item in items:
            yield scrapy.Request(url= 'https://www.itsu.com' + item, callback=self.parse_item)

    def parse_item(self, response):
        nutrients = response.xpath('//dl[@class="nutrition-facts grid-4"]/div')
        nutrient_dict = {}
        for nutrient in nutrients:
            nutrient_dict.update({
                nutrient.xpath('normalize-space(.//dt[@class="fact-title"]/text())').get():
                nutrient.xpath('normalize-space(.//dd[@class="fact-description"]/text())').get()})
        item_dict =  {
            'item_name': response.xpath('normalize-space(//h1[@class="h2 secondary-name"]/text())').get(),
            'item_description': response.xpath('normalize-space(//p[@class="description"]/text())').get(),
            'rest_name': 'Itsu',
            'collection_date': date.today().strftime("%b-%d-%Y"),
            # 'menu_section': response.request.meta['menu_section'],
        }
        item_dict.update(nutrient_dict)
        yield item_dict
