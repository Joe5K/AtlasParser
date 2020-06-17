import pymongo
import logging
# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


class MongoArticlePipeline:

    def __init__(self, mongo_uri, mongo_db, mongo_collection_name):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db
        self.mongo_collection_name = mongo_collection_name

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE'),
            mongo_collection_name=crawler.settings.get('MONGO_COLLECTION_NAME')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]
        self.db[self.mongo_collection_name].delete_many({})

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        self.db[self.mongo_collection_name].insert_one(dict(item))
        return item

class MongoCommentsPipeline:

    def __init__(self, mongo_uri, mongo_db, mongo_collection_name):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db
        self.mongo_collection_name = mongo_collection_name

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE'),
            mongo_collection_name=crawler.settings.get('MONGO_COLLECTION_NAME')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        link = item['link']
        del item['link']
        self.db[self.mongo_collection_name].update_one({'link': link}, {'$push': {'comments': item}})
        return item