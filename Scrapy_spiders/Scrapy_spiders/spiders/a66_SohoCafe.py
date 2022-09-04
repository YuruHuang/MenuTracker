from datetime import date

import scrapy


class A66SohocafeSpider(scrapy.Spider):
    name = '66_SohoCafe'
    allowed_domains = ['sohocoffee.com']
    start_urls = ['https://sohocoffee.com/menu/breakfast/']

    def parse(self,response):
        category_links = response.xpath('//ul[@id="menu-food-menus"]/li/a/@href').getall()
        for cat_link in category_links:
            yield scrapy.Request(url = cat_link, callback=self.parse_cat)
    
    def parse_cat(self, response):
        items = response.xpath('//a[contains(@class, "data__set-btn")]/@href').getall()
        category = response.request.url.split('/')[-2]
        for item in items: 
            yield scrapy.Request(url = item, callback=self.parse_item, meta = {'category': category})
    
    def parse_item(self, response): 
        table = response.xpath('//tr')
        item_name = response.xpath('//span[@class="fl-heading-text"]/text()').get()
        item_dict = {
            'collection_date': date.today().strftime("%b-%d-%Y"),
            'rest_name': 'Soho Coffee',
            'item_name': item_name , 
            'menu_section': response.meta.get('category'),
            'item_description': response.xpath('normalize-space(//div[@class="fl-module-content fl-node-content"]/p/text())').get()}
        for row in table: 
            header = row.xpath('.//td/strong/text()').get()
            values = [value for value in row.xpath('.//td/text()').getall() if value !='']
            if len(values) == 1:
                values = values[0]
                item_dict.update({header: values})
            elif len(values) ==2: 
                item_dict.update({
                    header+'_100g': values[0],
                    header + '_perserving': values[1]
                })
        yield item_dict
        # # add all the rows that are not milk related 
        # for keys, values in nutrition_dict.items():
        

