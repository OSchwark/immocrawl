import scrapy


class CarstensenImmobilienSpider(scrapy.Spider):
    name = "Carstensen-Immobilien"

    def start_requests(self):
        urls = [
            'https://www.immobilien-carstensen.de/angebote.xhtml'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        article_links = response.xpath('//div[@class=\'list-object\']//a/@href')
        yield from response.follow_all(article_links, self.parse_details_page)

    def parse_details_page(self, response):
        table_rows = response.xpath('//div[@class=\'details-mobile\']//tr')
        details = {}
        for row in table_rows:
            details[row.xpath('./td[1]//text()').get()] = row.xpath('./td[2]//text()').get()
        print(details)
        yield {
            'url': response.url,
            'title': response.xpath('//div[@class=\'detail\']/h2/text()').get(),
            'price': self.get_price(details),
            'images': response.xpath('//div[contains(@class,\'fotorama\')]/img/@src').getall()
        }

    def get_price(self, details_dict):
        for key,value in details_dict.items():
            if key.__contains__("preis") or key.__contains__("Preis") or key.__contains__("Miete") or key.__contains__("miete"):
                return value + " (" + key + ")"

        return ""
