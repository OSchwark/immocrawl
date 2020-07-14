import scrapy


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
        yield {
            'url': response.url,
            'title': response.xpath('//h1/text()').get(),
            'price': response.xpath('//span[@class=\'preis\']/text()').get()
        }
