from datetime import date

import scrapy


class A72TimhortonsSpider(scrapy.Spider):
    name = '72_TimHortons'
    allowed_domains = ['timhortons.co.uk']
    start_urls = ['https://timhortons.co.uk/menu']

    def parse(self, response):
        categories = response.xpath('//div[@class="menu-items box-grid small-up-2 medium-up-3 large-up-4"]')
        for category in categories:
            items = category.xpath('./a')
            cat_name = items[0].xpath('./div/@class').get().replace('anchor', '')
            for item in items:
                item_name = item.xpath('./p/text()').get()
                id = item.xpath('./@href').get().replace('#', '')
                modal = response.xpath(f'//div[@id="{id}"]')
                vegetarian = modal.xpath('.//p[@class="calorie-disclaimer"]/text()').getall()
                nutrition = modal.xpath('.//dl')
                servingsize = nutrition.xpath('./dt[contains("Serving Size", text())]/parent::dl/dd/text()').get()
                item_dict = {
                    'collection_date': date.today().strftime("%b-%d-%Y"),
                    'rest_name': 'Tim Hortons',
                    'menu_section': cat_name,
                    'menu_id': id,
                    'item_name': item_name,
                    'servingsize': servingsize,
                    'vegetarian': vegetarian
                }
                for row in nutrition[1:]:
                    header = row.xpath('./dt/text()').get()
                    values = row.xpath('./dd/text()').getall()
                    # fix a bug in the website cold brew item
                    if len(values) == 2:
                        item_dict.update({header + '_perserving': values[0], header + '_percent': values[1]})
                    else:
                        if len(values) == 1:
                            if '%' in values[0]:
                                item_dict.update({header + '_percent': values[0]})
                            else:
                                item_dict.update({header + '_perserving': values[0]})
                yield item_dict
