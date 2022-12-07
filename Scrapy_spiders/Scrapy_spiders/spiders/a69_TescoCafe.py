from datetime import date

import scrapy


class A69TescocafeSpider(scrapy.Spider):
    name = '69_TescoCafe'
    allowed_domains = ['www.tesco.com']
    start_urls = ['https://www.tesco.com/zones/tesco-cafe']

    def parse(self, response):
        menus = response.xpath("//h2[contains('Browse our menus', text())]/parent::div/following-sibling::div[1]//a")
        for menu in menus:
            cat = menu.xpath('./@aria-label').get()
            menu_url = menu.xpath('./@href').get()
            yield scrapy.Request(url=menu_url, callback=self.parse_item, meta={'category': cat})

    def parse_item(self, response):
        category = response.request.meta['category']
        items = response.xpath('//div[@class="base-components__RootElement-sc-1mosoyj-1 styled-erqp9a-0 gwIwEm egixNm shared__Row-xzat31-0 dJbDMN beans-grid__row"]//section')
        for item in items:
            item_all = item.xpath('./@aria-label').get()
            calories = item_all.split(',')[-1].strip()
            desc = ','.join(item_all.split(',')[1:-1])
            item_name_all = item_all.split(',')[0].strip()
            yield {
                'collection_date': date.today().strftime("%b-%d-%Y"),
                'rest_name': 'Tesco Cafe',
                'menu_section': category,
                'item_name': item_name_all.split('£')[0],
                'item_description': desc,
                'kcal': calories,
            }
