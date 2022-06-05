from datetime import date

import scrapy


class A30GbkSpider(scrapy.Spider):
    name = '30_GBK'
    allowed_domains = ['menus.tenkites.com']
    start_urls = ['https://menus.tenkites.com/brg/gourmetburgerkitchen']

    def parse(self, response):
        categories = response.xpath(
            '//div[@class="tk-html-body"]/section[@class="k10-menus"]/div[@class="k10-body"]/div[@class="k10-all-courses"]/section')
        for category in categories:
            cat_name = category.xpath('.//h2[@class="k10-course__name-value"]/text()').get()
            items = category.xpath('.//div[@class="k10-recipe k10-recipe_menu-item "]')
            for item in items:
                item_dict = {
                    'collection_date': date.today().strftime("%b-%d-%Y"),
                    'rest_name': "GBK",
                    'menu_section': cat_name,
                    'item_name': item.xpath(
                        'normalize-space(string(.//h3[@class="k10-recipe__name k10-recipe__customise-button"]))').get(),
                    'item_description': item.xpath('normalize-space(string(.//div[@class="k10-recipe__desc "]))').get(),
                }
                rows = item.xpath('.//div[@class="k10-modal-perfect__table-row"]')
                for row in rows:
                    item_dict.update({
                        row.xpath(
                            'normalize-space(./div[@class="k10-modal-perfect__table-name k10-recipe__nutrient-name"]/text())').get():
                            row.xpath(
                                'normalize-space(./div[@class="k10-modal-perfect__table-value k10-recipe__nutrient-value"]/text())').get()
                    })
                yield item_dict
