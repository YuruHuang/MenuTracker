from datetime import date

import scrapy


class A73TopgolfSpider(scrapy.Spider):
    name = '73_TopGolf'
    allowed_domains = ['topgolf.com', 'topgolf.kitchencut.com']
    start_urls = ['https://topgolf.com/uk/food-and-drink/allergens/']

    def parse(self, response):
        url_menu = response.xpath('//section[@class="no-top-border"]//iframe/@src').get()
        yield scrapy.Request(url=url_menu, callback=self.parse_item)

    def parse_item(self, response):
        categories = response.xpath('//div[@class="table-responsive"]')
        for category in categories:
            cat_name = category.xpath('.//h4/text()').get()
            headers = category.xpath('.//th[contains(@class,"th")]/text()').getall()[0:10]
            items = category.xpath('.//tr[contains(@class,"jsDish")]')
            for item in items:
                values = item.xpath('./td/text()').getall()[0:10]
                item_dict = dict(zip(headers, values))
                allergens = item.xpath('./td[@class="active_allergen"]/span/a')
                allergen_string = ''
                for allergen in allergens:
                    allergen_name = allergen.xpath('./@data-original-title').get()
                    allergen_text = allergen.xpath('normalize-space(string())').get()
                    allergen_string = allergen_string + allergen_text + ' ' + allergen_name + ','
                item_dict.update(
                    {
                        'collection_date': date.today().strftime("%b-%d-%Y"),
                        'rest_name': 'Top Golf',
                        'menu_section': cat_name,
                        'allergens': allergen_string
                    }
                )
                yield item_dict
