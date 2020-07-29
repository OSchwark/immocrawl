# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Field
from scrapy.loader.processors import TakeFirst


class ImmocrawlItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    source = Field(output_processor=TakeFirst())
    id = Field(output_processor=TakeFirst())
    url = Field(output_processor=TakeFirst())
    title = Field(output_processor=TakeFirst())
    images = Field()
    price = Field(output_processor=TakeFirst())
    indexed_date = Field()
