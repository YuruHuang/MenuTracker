from datetime import date

import scrapy


class A63PieministerSpider(scrapy.Spider):
    name = '63_Pieminister'
    allowed_domains = ['pieminister.co.uk']
    start_urls = ['https://pieminister.co.uk/pies/',
                  'https://pieminister.co.uk/food/patties/']

    def parse(self, response):
        pies = response.xpath('//li[@class="pies-list__item"]/a/@href').getall()
        category = response.url.split('/')[-2]
        for pie in pies:
            yield scrapy.Request(url=pie, callback=self.parse_pie, meta={'cat': category})

    def parse_pie(self, response):
        nutrition = response.xpath('//div[@id="pie-nutrition"]//tbody/tr')
        ingredients = ' '.join(response.xpath('//div[@id="pie-ingredients"]/p').getall())
        nutrition_dict = {}
        for nutrition_row in nutrition:
            header = nutrition_row.xpath('./td[1]/text()').get()
            per100 = nutrition_row.xpath('./td[2]/text()').get()
            perserving = nutrition_row.xpath('./td[3]/text()').get()
            nutrition_dict.update({header + '_perserving': perserving, header + '_per100': per100})
        item_dict = {
            'rest_name': 'Pieminister',
            'collection_date': date.today().strftime("%b-%d-%Y"),
            'menu_section': response.meta['cat'],
            'item_name': response.xpath('//h1[@class="pie-overview__title"]/text()').get(),
            'item_description': response.xpath(
                'normalize-space(//span[@class="pie-overview__description"]/text())').get(),
            'ingredients': ingredients,
            'url': response.url
        }
        item_dict.update(nutrition_dict)
        yield item_dict
