import pymongo


# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

class MongoArticlePipeline:
    counter = 0
    def __init__(self, mongo_uri, mongo_db, mongo_collection_name):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db
        self.collection_name = mongo_collection_name

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
        self.db[self.collection_name].delete_many({})

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        to_insert = dict(item)
        to_insert['id'] = self.counter
        self.counter += 1
        self.db[self.collection_name].insert_one(to_insert)
        return item

class MongoCommentsPipeline:

    def __init__(self, mongo_uri, mongo_db, mongo_collection_name):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db
        self.collection_name = mongo_collection_name

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
        spider.start_urls = [f'{record["link"]}/diskuse/cas' for record in self.db[self.collection_name].find({})]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        link = item['link']
        del item['link']
        self.db[self.collection_name].update_one({'link': link}, {'$push': {'comments': item}})
        return item