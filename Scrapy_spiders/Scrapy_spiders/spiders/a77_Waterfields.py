from datetime import date

from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class A76WaterfieldsSpider(CrawlSpider):
    name = '77_Waterfields'
    allowed_domains = ['www.waterfields-bakers.co.uk']
    start_urls = ['https://www.waterfields-bakers.co.uk/category/our-products']

    rules = (
        Rule(LinkExtractor(restrict_xpaths='//div[@class="product-name"]/a'), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        rows = response.xpath('//div[@id="product-attributes"]//div[@class="row"]')
        item_dict = {
            'collection_date': date.today().strftime("%b-%d-%Y"),
            'rest_name': "Waterfield's",
            'menu_section': response.url.split('/')[-3],
            'item_name': response.xpath('//h1[@class="product-detail-name"]/text()').get(),
            'item_description': response.xpath('normalize-space(//div[@id="product-description"]/p/text())').get()
            # 'allergens': ''.join(response.xpath('//p/strong/text()').getall()).strip()
        }
        for row in rows[1:]:
            values = row.xpath('./div/text()').getall()
            if len(values) == 1:
                nutrient_header = row.xpath('./div/div/div/text()').get().strip()
                nutrient_value = values[0]
            else:
                nutrient_header = values[0]
                nutrient_value = values[1]
            if 'Salt' in nutrient_header:
                nutrient_header = 'salt'
            if '/' in nutrient_value:
                item_dict.update({
                    nutrient_header: nutrient_value.split('/')[0].strip(),
                    nutrient_header + '_100': nutrient_value.split('/')[1].strip()
                })
            else:
                item_dict.update({
                    nutrient_header: nutrient_value.strip()
                })
        yield item_dict
