# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo

class ScraperPipeline(object):

    def __init__(self):
        MONGO_URI = 'mongodb+srv://rauthag:4404Aa84847d@myservice-ddf5u.mongodb.net/test?retryWrites=true&w=majority'
        self.connection = pymongo.MongoClient(MONGO_URI)

        db = self.connection['SectorSK']
        self.collection = db['SectorSK_articles']

    def process_item(self, item, spider):
        self.collection.insert(dict(item))
        return item
