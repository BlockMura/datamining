# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from pymongo import MongoClient
from sqdatabase.batabase import BlogBase
from sqdatabase.model import BlogPost, Autors, Tags, Base
import scrapy
from scrapy.pipelines.images import ImagesPipeline


class GeekbrainPipeline(object):
    def __init__(self):
        mongo_url = 'mongodb://localhost:27017'
        client = MongoClient(mongo_url)
        self.gb_bd = client.geekbrains

    def process_item(self, item, spider):
        collection = self.gb_bd[spider.name]
        collection.insert_one(item)
        return item


class AvitoPhotosPipelines(ImagesPipeline):

    def get_media_requests(self, item, info):
        if item['photos']:
            for img in item['photos']:
                try:
                    yield scrapy.Request(img)
                except Exception as e:
                    pass

    def item_completed(self, results, item, info):
        if results:
            item['photos'] = [itm[1] for itm in results if itm[0]]
        return item
