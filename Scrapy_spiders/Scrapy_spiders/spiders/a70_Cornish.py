# import re
from datetime import date
import scrapy
import urllib.parse


class A70CornishSpider(scrapy.Spider):
    name = '70_Cornish'
    allowed_domains = ['thecornishbakery.com']
    start_urls = ['https://thecornishbakery.com/pages/pasties-by-post']

    def parse(self, response):
        items = response.xpath('//a[@class="product-link is-not-relative"]/@href').getall()
        for item in items:
            item_url = 'https://thecornishbakery.com' + item
            yield scrapy.Request(url=item_url, callback=self.parse_item)


    def parse_item(self, response):
        # nutrition = response.xpath('//table/tbody/tr')
        # nutrition_dict = {}
        # for row in nutrition:
        #     values = row.xpath('./td/text()').getall()
        #     nutrition_dict.update({values[0]+'_100':values[1],
        #                            values[0]+'_perserving': values[2]})
        ingredients = response.xpath('(//span[@class="metafield-multi_line_text_field"])[1]/text()').getall()
        allergens = [allergen for allergen in ingredients if 'Allergens:' in allergen][0]
        item_dict = {
            'collection_date': date.today().strftime("%b-%d-%Y"),
            'rest_name': 'The Cornish Bakery',
            'item_name': response.xpath('normalize-space(//h1[@class="product__title"]/text())').get(),
            'item_description': ''.join(
                response.xpath('//div[@class="product-description rte"]//span/text()').getall()),
            'price': response.xpath('normalize-space(//div[@class="product__price"]/span/text())').get(),
            'ingredients': ''.join(ingredients),
            'allergens': allergens,
            # 'servingsize':  re.compile('\d+').search(response.xpath('(//th[@scope="col"])[3]/p[1]/text()').get()).group(0),
            # 'nutrition_url': 'https:'+ response.xpath('//div[@class="image__fill fade-in-image"]/@style').get().split('url(')[1].replace(');',''),
            'product_url': response.url
        }
        # item_dict.update(nutrition_dict)
        yield item_dict



# for the ones with the custom builder -> small batch of code to download the data for individual pastries 

# builder_url = 'https://thecornishbakery.com/apps/builder?b=nhNf7NXilUGOQUGzaCeS7tL1'
# urls = response.xpath('//div[@class="bxp-owl-item"]//a/@title-strip').getall()
# urls = list(set(urls))
# for url in urls: 
#     content = urllib.parse.unquote(url)
#     content_page = scrapy.Selector(text = content)

