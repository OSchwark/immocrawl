import logging
from datetime import datetime

import scrapy
from bs4 import BeautifulSoup
from requests_html import HTMLSession
from scrapy.loader import ItemLoader

from immocrawl.items import ImmocrawlItem


class ObrockSpider(scrapy.Spider):
    name = "Obrock"

    def __init__(self, name=None, **kwargs):
        super().__init__(name, **kwargs)
        logging.getLogger('websockets.protocol').setLevel(logging.ERROR)
        logging.getLogger('websockets.server').setLevel(logging.ERROR)
        logging.getLogger('pyppeteer').setLevel(logging.ERROR)

    def start_requests(self):
        urls = [
            'https://www.obrock.de/angebote/suchen/'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        article_links = response.xpath("//a[@class='immo-listing__image']")
        yield from response.follow_all(article_links, self.parse_details_page)
        yield from response.follow_all(response.xpath("//a[@class='next page-numbers']"), self.parse)

    def parse_details_page(self, response):
        loader = ItemLoader(item=ImmocrawlItem(), selector=response)
        # loader.add_xpath('title', "//h1/text()")
        # loader.add_xpath('images', "//img[@sizes]/@src")
        loader.add_value('url', response.url)
        loader.add_xpath('price',  "//span[contains(@class, 'font-weight-semibold') and contains(.,'€')]/text()")

        session = HTMLSession()
        resp = session.get(response.url, timeout=5)
        resp.html.render(wait=0.6)

        loader.add_value('id', resp.html.xpath('//span[@title="Objekt-Nr"]/../span[@class="value"]')[0].text)
        loader.add_value('source', self.name)
        loader.add_value('indexed_date', datetime.now())
        loader.add_xpath('images', '''//img[contains(@src, 'immo.screenwork.de/immobilienbilder')]/@src''')
        yield loader.load_item()
