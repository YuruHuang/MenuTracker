from datetime import date

import scrapy


class A85RealgreekSpider(scrapy.Spider):
    name = '85_RealGreek'
    allowed_domains = ['www.therealgreek.com']
    start_urls = ['https://www.therealgreek.com/menu/']

    def parse(self, response):
        categories = response.xpath('//h2[@class="h1 text-left scrl-mg-body"]')
        for category in categories:
            cat_name = category.xpath('./text()').get()
            items = category.xpath(
                '(./parent::div/following-sibling::div[@class="col-sm-6 col-md-6 col-lg-6"])[1]/div/div')
            for item in items:
                yield {
                    'collection_date': date.today().strftime("%b-%d-%Y"),
                    'rest_name': 'The Real Greek',
                    'menu_section': cat_name,
                    'item_name': item.xpath('.//h4[@class="the_dish_title"]/text()').get(),
                    'price': item.xpath('.//h4[@class="price"]/text()').get(),
                    'item_description': item.xpath('.//div[@class="the_dish_description"]/p/text()').get(),
                    'dietary': item.xpath('normalize-space(.//div[@class="the_dietary_info"]/p/text())').get(),
                }
