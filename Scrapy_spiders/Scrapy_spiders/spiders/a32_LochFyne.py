import scrapy


class A32LochfyneSpider(scrapy.Spider):
    name = '32_LochFyne'
    allowed_domains = ['www.lochfyneseafoodandgrill.co.uk']
    start_urls = ['https://www.lochfyneseafoodandgrill.co.uk/menu/a-la-carte-menu/']

    def parse(self, response):
        menu_sections = response.xpath('//div[@class="module rich-text rich-text"]//h2')
        for menu_section in menu_sections:
            menu_section_name = menu_section.xpath('./text()').get()
            menu_section_description = menu_section.xpath('./following-sibling::p/text()').get()
