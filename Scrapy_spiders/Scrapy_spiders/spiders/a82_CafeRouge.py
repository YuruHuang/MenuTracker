from datetime import date

import scrapy


class A82CaferougeSpider(scrapy.Spider):
    name = '82_CafeRouge'
    allowed_domains = ['www.caferouge.com', 'menus.tenkites.com']
    start_urls = ['https://menus.tenkites.com/thebigtg/mobilemenuscaferouge02']

    def parse(self, response):
        cat_links = response.xpath('//div[@class="k10-menu-selector__option"]/span')
        cat_links = set(cat_links)
        for cat_link in cat_links:
            link = cat_link.xpath('./@data-menu-identifier').get()
            name = cat_link.xpath('normalize-space(./span/text())').get()
            yield scrapy.Request(
                url=f'https://menus.tenkites.com//thebigtg/mobilemenuscaferouge02?cl=true&mguid={link}&internalrequest=true',
                callback=self.parse_item, meta={'menu_name': name})

    def parse_item(self, response):
        i = 1
        menu_name = response.request.meta['menu_name']
        categories = response.xpath('//section[@class="k10-course k10-course_collapsed"]')
        for category in categories:
            cat_name = category.xpath('normalize-space(.//div[@class="k10-course__name"]/text())').get()
            items = category.xpath('.//span[contains(@class,"__name")]')
            for item in items:
                item_name = item.xpath('normalize-space(./text())').get()
                item_desc = item.xpath('normalize-space(./parent::div/div[contains(@class,"__desc")]/text())').get()
                item_dict = {
                    'collection_date': date.today().strftime("%b-%d-%Y"),
                    'rest_name': "Cafe Rouge",
                    'menu_section': cat_name,
                    'item_name': item_name,
                    'item_description': item_desc,
                    'menu_name': menu_name
                }
                table = response.xpath(f'(//table)[{i}]')
                rows = table.xpath('.//tr[@class="k10-popover__nutrients-table__tr"]')
                i += 1
                for row in rows:
                    item_dict.update({
                        row.xpath('normalize-space(./td[1]/text())').get():
                            row.xpath('normalize-space(./td[2]/text())').get()
                    })
                yield item_dict
