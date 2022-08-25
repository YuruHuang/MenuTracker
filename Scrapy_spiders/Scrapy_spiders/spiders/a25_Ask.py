from datetime import date

import scrapy


class A25AskSpider(scrapy.Spider):
    name = '25_Ask'
    allowed_domains = ['www.askitalian.co.uk']
    start_urls = ['https://www.askitalian.co.uk/menus/full-menu/']
    # start_urls = ['https://www.askitalian.co.uk/wp-json/menus/get_menus_from_ids?ids=4182,4448,4632,4594']

    def parse(self, response):
        menu_ids = response.xpath('//div[@class="js-menus  c-menus"]/@data-menus').get().replace('[','').replace(']','')
        query_url = f'https://www.askitalian.co.uk/wp-json/menus/get_menus_from_ids?ids={menu_ids}'
        yield scrapy.Request(url = query_url, callback = self.parse_cat)

    def parse_cat(self, response):
        menu_names = response.json().get('data')
        for menu_name in menu_names:
            name = menu_name.get('name')
            yield scrapy.Request(
                url=f'https://www.askitalian.co.uk/wp-json/menus/get_menu_from_name?name={name}',
                callback=self.parse_menu,
                meta={'menuName': name}
            )

    def parse_menu(self, response):
        menu_sections = response.json().get('data').get('menu_sections')
        for menu_section in menu_sections:
            menu_section_name = menu_section.get('section_title')
            items = menu_section.get('items')
            if items is None:
                subsections = menu_section.get('subsections')
                for subsection in subsections:
                    items = subsection.get('items')
                    for item in items:
                        yield {
                            'collection_date': date.today().strftime("%b-%d-%Y"),
                            'rest_name': "Ask",
                            'menu_name': response.request.meta['menuName'],
                            'menu_section': menu_section_name,
                            'item_name': item.get('name'),
                            'item_id': item.get('id'),
                            'kcal': item.get('calorie_information'),
                            'item_description': item.get('description'),
                            'price': item.get('prices').get('mid_price_point'),
                            'dietary': item.get('dietary')
                        }
            else:
                for item in items:
                    yield {
                        'collection_date': date.today().strftime("%b-%d-%Y"),
                        'rest_name': "Ask",
                        'menu_name': response.request.meta['menuName'],
                        'menu_section': menu_section_name,
                        'item_name': item.get('name'),
                        'item_id': item.get('id'),
                        'kcal': item.get('calorie_information'),
                        'item_description': item.get('description'),
                        'price': item.get('prices').get('mid_price_point'),
                        'dietary': item.get('dietary')
                    }
