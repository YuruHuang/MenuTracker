from datetime import date

import scrapy


class A50CrusshSpider(scrapy.Spider):
    name = '50_Crussh'
    allowed_domains = ['crussh.com']
    start_urls = ['https://crussh.com']

    def parse(self, response):
        cat_links = response.xpath('//a[@class="title"]/@href').getall()
        for cat_link in cat_links:
            yield scrapy.Request(url=cat_link, callback=self.parse_item)

    def parse_item(self, response):
        items = response.xpath('//div[@class="item"]')
        for item in items:
            nutrition = item.xpath('./div[@class="data nutritionFacts"]')
            headers = nutrition.xpath('./table/thead/tr/th/text()').getall()
            rows = nutrition.xpath('./table/tbody/tr')
            nutrient_dict = {}
            for row in rows:
                nutrient = row.xpath('./td[1]/text()').get()
                for i in range(2, (len(headers) + 2)):
                    try:
                        value = row.xpath(f'./td[{i}]/text()').get().replace(',', '.')
                    except:
                        value = None
                    key = nutrient + '_' + headers[i - 2]
                    nutrient_dict.update({key: value})
            item_dict = {
                'rest_name': 'Crussh',
                'collection_date': date.today().strftime("%b-%d-%Y"),
                'menu_section': response.url.split('/')[-2],
                'item_name': item.xpath('./div[@class="header"]/h3/text()').get(),
                'item_description': item.xpath('./div[@class="header"]/p[@class="shortDescription"]/text()').get(),
                'price': item.xpath('./p[@class="price"]/text()').get(),
                'allergens': item.xpath('.//div[@class="data allergens"]/text()').get()
            }
            item_dict.update(nutrient_dict)
            yield item_dict
