import re
from datetime import date

import scrapy


class A20ChefbrewerSpider(scrapy.Spider):
    name = '20_ChefBrewer'
    allowed_domains = ['smartchef.co.uk']
    start_urls = ['https://www.smartchef.co.uk/brands/ChefBrewer?siteid=6145']

    def parse(self, response):
        menus = response.xpath('//li[contains(@class, "nav-item")]/@id').getall()
        menu_ids = [menu.replace('navBar-', '') for menu in menus]
        for menu_id in menu_ids:
            yield scrapy.Request(
                url=f'https://www.smartchef.co.uk/Brands/ChefBrewerMenuItems?menuid={menu_id}&filter=%27%27',
                callback=self.parse_item,
                meta={'menu_id': menu_id}
            )

    def parse_item(self, response):
        sections = response.xpath('//div[@class="tabContent"]')
        for section in sections:
            section_name = section.xpath('./h3[@class="section-head p-1"]/text()').get()
            subsections = section.xpath('./div[@class="subTabContent"]')
            for subsection in subsections:
                subsection_name = subsection.xpath('./preceding-sibling::h3[@class="p-1"]/text()').get()
                items = subsection.xpath('./div[@class="menuItem"]')
                for item in items:
                    item_data = item.xpath('./p/span/text()').getall()
                    try:
                        kcal = re.search('([0-9]* kcal)', item_data[1]).group(1).replace(' kcal', '')
                    except:
                        kcal = None
                    yield {
                        'rest_name': 'Chef and Brewer',
                        'menu_id': response.request.meta['menu_id'],
                        'menu_section': section_name + ', ' + subsection_name,
                        'collection_date': date.today().strftime("%b-%d-%Y"),
                        'item_name': item_data[0],
                        'item_description': item_data[1],
                        'allergens': item_data[2],
                        'kcal': kcal
                    }
