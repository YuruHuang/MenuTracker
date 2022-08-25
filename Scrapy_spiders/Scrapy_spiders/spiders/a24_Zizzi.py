from datetime import date

import scrapy


class A24ZizziSpider(scrapy.Spider):
    name = '24_Zizzi'
    allowed_domains = ['www.zizzi.co.uk', 'www.zizzi.com']
    start_urls = ['https://www.zizzi.co.uk/menus/full-menu/']
    # start_urls = ['https://www.zizzi.com/wp-json/menus/get_menus_from_ids?ids=6597,6662,6661,6664,6663,6560,6569'] # Ah. IDs change all the time, how to build code resillence? check network requests again

    def parse(self, response):
        menu_ids = response.xpath('//div[@class="js-menus  c-menus"]/@data-menus').get().replace('[','').replace(']','')
        query_url = f'https://www.zizzi.com/wp-json/menus/get_menus_from_ids?ids={menu_ids}'
        yield scrapy.Request(url = query_url, callback = self.parse_cat)
    
    def parse_cat(self, response): 
        menu_names = response.json().get('data')
        for menu_name in menu_names:
            name = menu_name.get('name')
            yield scrapy.Request(
                url=f'https://www.zizzi.com/wp-json/menus/get_menu_from_name?name={name}',
                callback=self.parse_menu,
                meta={'menuName': name}
            )

    def parse_menu(self, response):
        menu_sections = response.json().get('data').get('menu_sections')
        for menu_section in menu_sections:
            menu_section_name = menu_section.get('section_title')
            print(menu_section_name)
            items = menu_section.get('items')
            for item in items:
                yield {
                    'collection_date': date.today().strftime("%b-%d-%Y"),
                    'rest_name': "Zizzi",
                    'menu_name': response.request.meta['menuName'],
                    'menu_section': menu_section_name,
                    'item_name': item.get('name'),
                    'item_id': item.get('id'),
                    'kcal': item.get('calorie_information'),
                    'item_description': item.get('description'),
                    'price': item.get('prices').get('core_price_point'),
                    'dietary': item.get('dietary')
                }
