# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import logging

from itemadapter import ItemAdapter
import pymongo

from scrapy.utils.project import get_project_settings
from scrapy.exceptions import DropItem


class MongoDBPipeline(object):

    def __init__(self):
        settings = get_project_settings()
        connection = pymongo.MongoClient(
            settings['MONGODB_SERVER'],
            settings['MONGODB_PORT']
        )
        db = connection[settings['MONGODB_DB']]
        self.collection = db[settings['MONGODB_COLLECTION']]

    def process_item(self, item, spider):
        valid = True
        for data in item:
            if not data:
                valid = False
                raise DropItem("Missing {0}!".format(data))
        if valid:
            self.collection.insert(dict(item))
            logging.info("Real estate entered")
        return item


class DuplicatesPipeline:
    def __init__(self):
        settings = get_project_settings()
        connection = pymongo.MongoClient(
            settings['MONGODB_SERVER'],
            settings['MONGODB_PORT']
        )
        db = connection[settings['MONGODB_DB']]
        self.collection = db[settings['MONGODB_COLLECTION']]
        self.ids_seen = set()
        for item in self.collection.find({}, {'id': 1, 'source': 1}):
            print(item.get('source'))
            print(item.get('id'))
            self.ids_seen.add(item.get('source') + item.get('id'))

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        if adapter['source']+adapter['id'] in self.ids_seen:
            raise DropItem("Duplicate item found: %r" % item)
        else:
            self.ids_seen.add(adapter['source']+adapter['id'])
            return item


class ImmocrawlPipeline:
    def process_item(self, item, spider):
        return item
