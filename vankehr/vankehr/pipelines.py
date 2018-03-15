# -*- coding: utf-8 -*-

from pymongo import MongoClient
from scrapy.conf import settings
from .items import VankeItem
from traceback import format_exc


class VankehrPipeline(object):

    def __init__(self,mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db
        self.client = None
        self.db = None

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri = crawler.settings.get('MONGO_URI'),
            mongo_db = crawler.settings.get('MONGODB_DATABASE','items')
            )

    def open_spider(self,spider):
        self.client = MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]
        self.db['vanke_hr_info'].ensure_index('id',unique=True)

    def close_spider(self,spider):
        self.client.close()

    def process_item(self, item, spider):
        try:
            self.db['vanke_hr_info'].update({'id':item['id_position']},{'$set':item},upsert=True)
        except Exception as e:
            spider.logger.error(format_exc())

        return item
