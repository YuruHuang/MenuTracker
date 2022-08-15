import scrapy
from datetime import date
import re

class A32LochfyneSpider(scrapy.Spider):
    name = '32_LochFyne'
    allowed_domains = ['www.lochfyneseafoodandgrill.co.uk']
    start_urls = ['https://www.lochfyneseafoodandgrill.co.uk/menu/a-la-carte-menu/',
                  'https://www.lochfyneseafoodandgrill.co.uk/menu/non-gluten-menu/',
                  'https://www.lochfyneseafoodandgrill.co.uk/menu/childrens-menu/']

    def parse(self, response):
        menu_reference = response.request.url.split('/')[-2]
        menu_sections = response.xpath('//div[@class="module rich-text rich-text"]//h2/text()').getall()
        for menu_section in menu_sections:
            position = int(float(response.xpath(f'count(//h2[text()="{menu_section}"]/preceding-sibling::h2) + 1').get()))
            items = response.xpath(f'//h4[count(preceding-sibling::h2) = {position}]')
            for item in items:
                item_description = item.xpath('normalize-space(./following-sibling::p/text())').get()
                kcals = re.findall('\([0-9]+?-?[0-9]+ kcal',item_description)
                subitems = re.split("\\)",item_description)
                for i in range(len(kcals)):
                    yield{
                        'collection_date': date.today().strftime("%b-%d-%Y"),
                        'rest_name': "Loch Fyne",
                        'menu_reference': menu_reference,
                        'menu_section': menu_section,
                        'item_name': item.xpath('./text()').get(),
                        'item_description': subitems[i]+')',
                        'kcal': kcals[i].replace("(","")
                    }




