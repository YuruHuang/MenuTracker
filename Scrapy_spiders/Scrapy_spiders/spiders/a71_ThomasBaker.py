from datetime import date

import scrapy


class A71ThomasbakerSpider(scrapy.Spider):
    name = '71_ThomasBaker'
    allowed_domains = ['www.thomasthebaker.co.uk']
    start_urls = ['https://www.thomasthebaker.co.uk/shop/index.html']

    def parse(self, response, **kwargs):
        links = response.xpath('//a/@href').getall()
        shop_links = set([link for link in links if '/shop/' in link])
        for shop_link in shop_links:
            yield scrapy.Request(url='https://www.thomasthebaker.co.uk' + shop_link,
                                 callback=self.parse_cat)

    def parse_cat(self, response):
        cat_name = response.url.split('/')[-2]
        items = response.xpath('//div[@class="products__item "]/a/@href').getall()
        for item in items:
            yield scrapy.Request(url='https://www.thomasthebaker.co.uk' + item,
                                 callback=self.parse_item,
                                 meta={'cat': cat_name})

    def parse_item(self, response):
        item_dict = {
            'collection_date': date.today().strftime("%b-%d-%Y"),
            'rest_name': 'Thomas the Baker',
            'menu_section': response.meta['cat'],
            'item_name': response.xpath('//div[@class="product__info"]/h1/text()').get(),
            'price': response.xpath('//div[@class="product__info__price"]/p/strong/text()').get(),
            'item_description': response.xpath('//div[@class="product__info__snippet"]/p/text()').getall(),
            'allergens': response.xpath('//div[@id="allergens"]//p/text()').get(),
            'ingredients': response.xpath('//div[@class="product__extras__item product__ingredients"]//p/text()').get(),
            'servingsize': response.xpath('//p[@class="product__info__weight"]/text()').get(),
            'url': response.url
        }
        nutrition = response.xpath('//table/tbody/tr')
        for row in nutrition:
            values = row.xpath('./td/text()').getall()
            item_dict.update({values[0] + '_100': values[1]})
        yield item_dict
