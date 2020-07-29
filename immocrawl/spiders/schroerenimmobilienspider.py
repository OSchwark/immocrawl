from datetime import datetime

import scrapy
from scrapy.loader import ItemLoader

from immocrawl.items import ImmocrawlItem


class SchroerenImmobilienSpider(scrapy.Spider):
    name = "Schroeren-Immobilien"

    def start_requests(self):
        urls = [
            'https://www.schroeren-immobilien.de/objekte/'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        article_links = response.xpath('//article//h2/a/@href')
        yield from response.follow_all(article_links, self.parse_details_page)

    def parse_details_page(self, response):
        loader = ItemLoader(item=ImmocrawlItem(), selector=response)
        loader.add_xpath('title', "//h1/text()")
        loader.add_xpath('images', "//img[@sizes]/@src")
        loader.add_value('url', response.url)
        loader.add_xpath('price',  '//span[@class=\'preis\']/text()')
        loader.add_xpath('id', '//article[1]/@id')
        loader.add_value('source', self.name)
        loader.add_value('indexed_date', datetime.now())
        yield loader.load_item()
