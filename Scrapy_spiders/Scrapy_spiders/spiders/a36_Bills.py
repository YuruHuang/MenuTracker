from datetime import date

import scrapy


class A36BillsSpider(scrapy.Spider):
    name = '36_Bills'
    allowed_domains = ['menus.tenkites.com']
    start_urls = ['https://menus.tenkites.com/bills/bills03']

    # def parse(self, response):
    #     cat_links = response.xpath('//div[@class="k10-menu-selector__options"]//div/@data-menu-identifier').getall()
    #     cat_links = set(cat_links)
    #     for cat_link in cat_links:
    #         # print(cat_link)
    #         yield scrapy.Request(
    #             url=f'https://menus.tenkites.com//bills/bills02?cl=true&mguid={cat_link}&internalrequest=true',
    #             callback=self.parse_item)

    def parse(self, response):
        i = 1
        categories = response.xpath('//div[contains(@class, "k10-course_level_1")]')
        for category in categories:
            cat_name = category.xpath('normalize-space(.//div[@class="k10-course__name k10-w-course__name k10-course__name_level_1"]/text())').get()
            print(cat_name)
            # subcategories = category.xpath('.//div[@class="k10-course k10-course_level_2"]')
            # for subcat in subcategories: 
            # sub_cat_name = subcat.xpath('normalize-space(.//div[@class="k10-course__name k10-w-course__name_level_2 k10-course__name_level_2"]/text())').get()
            items = category.xpath('.//div[contains(@class,"grid-item")]')
            for item in items:
                item_dict = {
                        'collection_date': date.today().strftime("%b-%d-%Y"),
                        'rest_name': "Marstons",
                        'menu_section': cat_name,
                        'item_name': item.xpath('normalize-space(.//div[@class="k10-recipe__name k10-w-recipe__name"]/text())').get(), 
                        'item_description': item.xpath('normalize-space(.//span[@class="k10-recipe__desc k10-w-recipe__desc"]/text())').get()
                    }
                table = response.xpath(f'(//table)[{i}]')
                rows = table.xpath('.//tr[@class="k10-table__tr"]')
                i += 1
                for row in rows:
                    item_dict.update({
                        row.xpath('normalize-space(./td[1]/text())').get():
                            row.xpath('normalize-space(./td[2]/text())').get()
                    })
                yield item_dict
